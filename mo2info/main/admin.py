from django.contrib import admin

from .models import BowDamageTrial, BowDamagePredictor


@admin.register(BowDamageTrial)
class BowDamageTrialAdmin(admin.ModelAdmin):
    ...


@admin.register(BowDamagePredictor)
class BowDamagePredictorAdmin(admin.ModelAdmin):
    ...
