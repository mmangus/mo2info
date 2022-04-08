from django.core.validators import MinValueValidator
from django.db import models

class BowDamageTrial(models.Model):
    class BowTypeChoices(models.TextChoices):
        ASYM = "ASYM", "Asymmetric"
        LONG = "LONG", "Long"
        SHORT = "SHORT", "Short"

    bow_type = models.CharField(max_length=5, choices=BowTypeChoices.choices)
    range = models.FloatField(
        validators=[MinValueValidator(0.1)],
        help_text="The range from the bow's tooltip"
    )
    durability_current = models.FloatField(
        validators=[MinValueValidator(0.1)],
        help_text="Remaining durability before starting the trial"
    )
    durability_max = models.FloatField(
        validators=[MinValueValidator(0.1)],
        help_text="Maximum durability of the bow (second number in tooltip)"
    )
    mean_damage = models.FloatField(
        validators=[MinValueValidator(0.0)],
        help_text="The average damage per shot to the target dummy's head"
    )

    def __str__(self) -> str:
        return f"{self.bow_type} @ {self.range}: {self.mean_damage}"
