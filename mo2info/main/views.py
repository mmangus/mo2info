import csv

from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import CreateView, FormView, ListView, TemplateView

from .models import BowDamagePredictor, BowDamageTrial


class HomeView(TemplateView):
    """Lists models under development"""

    template_name = "main/home.html"


class BowDamageTrialCreateView(CreateView):
    """Records bow type, durability, range, and damage dealth"""

    model = BowDamageTrial
    fields = [
        "bow_type",
        "durability_current",
        "durability_max",
        "range",
        "damage_log",
    ]

    def get_success_url(self) -> str:
        return reverse("bow-damage-contribute")


class BowDamagePredictorSummaryView(TemplateView):
    """Lists summary data for alternative bow damage models"""

    template_name = "main/predictor_summary.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["summaries"] = []
        for predictor in BowDamagePredictor.objects.all():
            context["summaries"].append((str(predictor), predictor.summary))
        return context


# TODO install DRF and use its serializer layer + React client
class BowDamagePredictionForm(ModelForm):
    def clean(self):
        # this is a silly hack to show you the result as if it were a
        #  form error, which conveniently takes you back to the form with
        #  the previous values still filled in
        cleaned_data = super().clean()
        # FIXME what really matters seems to be arrow type not bow type?
        if cleaned_data["bow_type"] == "LONG":
            filter = {"bow_type": "LONG"}
        else:
            filter = {"bow_type__in": ["SHORT", "ASYM"]}
        # TODO come up w/ a strategy to dynamically select the best model
        predictor, _ = BowDamagePredictor.objects.get_or_create(
            formula="mean_damage ~ range", queryset_filter=filter
        )
        damage = predictor.predict({"range": [cleaned_data["range"]]})[0]
        raise ValidationError(
            f"Estimated average damage per shot: {round(damage)}"
        )

    class Meta:
        model = BowDamageTrial
        fields = ["bow_type", "range"]


class BowDamagePredictionView(FormView):
    form_class = BowDamagePredictionForm
    template_name = "main/predict.html"


class BowDamageTrialDownloadView(ListView):
    """Allows downloading all the bow damage data as a CSV"""

    model = BowDamageTrial

    def render_to_response(self, context, **response_kwargs):
        values_as_list = context["object_list"].values()
        if not values_as_list:
            raise BowDamageTrial.DoesNotExist()

        response = HttpResponse(
            content_type="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=bow-damage.csv"
            },
        )
        csv_writer = csv.writer(response)
        csv_writer.writerow(k for k in values_as_list[0].keys())
        for obj in values_as_list:
            csv_writer.writerow(obj.values())

        return response
