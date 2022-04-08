from django.forms import ModelForm

from .models import BowDamageTrial

class BowDamageTrialForm(ModelForm):
    class Meta:
        model = BowDamageTrial
