import re

from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

DAMAGE_LOG_RE = re.compile(r"((\d+)(?:\s*)){10}")

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
    damage_log = models.TextField(
        validators = [
            RegexValidator(
                DAMAGE_LOG_RE,
                message="Enter just the 10 numbers, 1 number per line"
            )
        ]
    )
    mean_damage = models.FloatField(
        validators=[MinValueValidator(0.0)],
        help_text="The average damage per shot to the target dummy's head"
    )

    def __str__(self) -> str:
        return f"{self.bow_type} @ {self.range}: {self.mean_damage}"


    def save(self, *args, **kwargs) -> None:
        self.mean_damage = sum(
            map(int, self.damage_log.split())
        ) / 10
        return super().save(*args, **kwargs)
