from django.contrib import admin

from .models import BowDamageTrial


@admin.register(BowDamageTrial)
class BowDamageTrialAdmin(admin.ModelAdmin):
    ...
