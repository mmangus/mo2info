from django.urls import reverse
from django.views.generic import CreateView

from .models import BowDamageTrial

class BowDamageTrialCreateView(CreateView):
    model = BowDamageTrial
    fields = [
        "bow_type",
        "range",
        "durability_current",
        "durability_max",
        "damage_log",
    ]

    def get_success_url(self) -> str:
        return reverse('bow-damage-create')
