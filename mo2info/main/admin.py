from django.contrib import admin

from .models import BowDamagePredictor, BowDamageTrial


@admin.register(BowDamageTrial)
class BowDamageTrialAdmin(admin.ModelAdmin):
    ...


@admin.register(BowDamagePredictor)
class BowDamagePredictorAdmin(admin.ModelAdmin):
    ...
