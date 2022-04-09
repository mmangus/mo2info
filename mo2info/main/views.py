from django.urls import reverse
from django.views.generic import CreateView, TemplateView

from .models import BowDamageTrial, BowDamagePredictor


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
        return reverse('bow-damage-contribute')


class BowDamagePredictorSummaryView(TemplateView):
    template_name = "main/predictor_summary.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["summaries"] = []
        for predictor in BowDamagePredictor.objects.all():
            context["summaries"].append(
                (
                    str(predictor),
                    predictor.summary
                )
            )
        return context
