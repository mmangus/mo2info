import csv
import json

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.views.generic import CreateView, ListView, TemplateView

from .models import BowDamagePredictor, BowDamageTrial


class HomeView(TemplateView):
    template_name = "main/home.html"


class BowDamageTrialCreateView(CreateView):
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
    template_name = "main/predictor_summary.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["summaries"] = []
        for predictor in BowDamagePredictor.objects.all():
            context["summaries"].append((str(predictor), predictor.summary))
        return context


class BowDamageTrialDownloadView(ListView):
    model = BowDamageTrial

    def render_to_response(self, context, **response_kwargs):
        response = HttpResponse(
            content_type="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=bow_damage.csv"
            }
        )
        csv_writer = csv.writer(response)
        values_as_list = context["object_list"].values()
        if not values_as_list:
            raise BowDamageTrial.DoesNotExist()
        csv_writer.writerow(k for k in values_as_list[0].keys())
        for obj in values_as_list:
            csv_writer.writerow(obj.values())

        return response