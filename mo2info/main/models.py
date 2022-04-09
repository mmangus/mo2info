import re
from typing import Optional

from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from pandas import DataFrame
from statsmodels.formula.api import ols
from statsmodels.regression.linear_model import RegressionResultsWrapper

DAMAGE_LOG_RE = re.compile(r"((\d+)(?:\s*)){10}")


class BowDamageTrial(models.Model):
    class BowTypeChoices(models.TextChoices):
        ASYM = "ASYM", "Asymmetric"
        LONG = "LONG", "Long"
        SHORT = "SHORT", "Short"

    bow_type = models.CharField(max_length=5, choices=BowTypeChoices.choices)
    range = models.FloatField(
        validators=[MinValueValidator(0.1)],
        help_text="The range from the bow's tooltip",
    )
    durability_current = models.FloatField(
        validators=[MinValueValidator(0.1)],
        help_text="Remaining durability before starting the trial",
    )
    durability_max = models.FloatField(
        validators=[MinValueValidator(0.1)],
        help_text="Maximum durability of the bow (second number in tooltip)",
    )
    durability_pct = models.FloatField()
    damage_log = models.TextField(
        validators=[
            RegexValidator(
                DAMAGE_LOG_RE,
                message="Enter just the 10 numbers, 1 number per line",
            )
        ],
        help_text="Enter 1 number per line",
    )
    mean_damage = models.FloatField(
        validators=[MinValueValidator(0.0)],
        help_text="The average damage per shot to the target dummy's head",
    )

    def __str__(self) -> str:
        return f"{self.bow_type} @ {self.range}: {self.mean_damage}"

    def save(self, *args, **kwargs) -> None:
        # denormalizing bc we'll fit models to these values frequently
        self.mean_damage = sum(map(int, self.damage_log.split())) / 10
        # TODO proper validator
        assert (
            self.durability_current <= self.durability_max
        ), "Invalid durability"
        self.durability_pct = self.durability_current / self.durability_max
        return super().save(*args, **kwargs)


class BowDamagePredictor(models.Model):

    formula = models.CharField(max_length=500)
    queryset_filter = models.JSONField(default=dict)

    # TODO cache by predictor id and persist as long as the container does
    #  unless manually busted
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._cached_predictor: Optional[RegressionResultsWrapper] = None
        self._cached_summary: Optional[str] = None

    def prepare_dataframe(self) -> DataFrame:
        return DataFrame(
            BowDamageTrial.objects.filter(**self.queryset_filter).values()
        )

    def fit(self) -> Optional[RegressionResultsWrapper]:
        df = self.prepare_dataframe()
        if df.empty:
            self._cached_predictor = None
            self._cached_summary = "No Data"
            return

        self._cached_predictor = ols(formula=self.formula, data=df).fit()
        self._cached_summary = self._cached_predictor.summary().as_html()
        return self._cached_predictor

    @property
    def predictor(self) -> RegressionResultsWrapper:
        if not self._cached_predictor:
            self.fit()
        return self._cached_predictor

    @property
    def summary(self) -> str:
        if not self._cached_summary:
            self.fit()
        return self._cached_summary

    def predict(self, *args, **kwargs) -> list[float]:
        return list(self.predictor.predict(*args, **kwargs))

    def __str__(self) -> str:
        return f"{self.formula} for {self.queryset_filter}"
