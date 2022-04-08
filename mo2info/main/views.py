from django.views.generic import CreateView

from .models import BowDamageTrial

class BowDamageTrialCreateView(CreateView):
    model = BowDamageTrial
    success_url = "/mo2/bow-damage/contribute/"
    fields = [
        "bow_type",
        "range",
        "durability_current",
        "durability_max",
        "mean_damage",
    ]
