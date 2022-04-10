import re
from typing import Optional, TypedDict

from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from pandas import DataFrame
from statsmodels.formula.api import ols
from statsmodels.regression.linear_model import RegressionResultsWrapper

DAMAGE_LOG_RE = re.compile(r"((\d+)(?:\s*)){10}")


class BowDamageTrial(models.Model):
    """
    Records data about bow damage dealt to a target dummy over 10 shots
    """

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
    """
    Predicts bow damage using OLS regression
    """

    id: int  # stop type complaints for implicit int PK
    formula = models.CharField(max_length=500)
    queryset_filter = models.JSONField(default=dict)

    # We keep a cache of the model details by instance ID as a class attribute
    #  so we aren't re-computing it every time.
    class CachedPredictor(TypedDict):
        predictor: Optional[RegressionResultsWrapper]
        summary: str

    _instance_cache: dict[int, CachedPredictor] = {}

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if self.id not in self._instance_cache:
            self.update_and_cache()

    def update_and_cache(self) -> None:
        self._instance_cache[self.id] = self._fit()

    def _prepare_dataframe(self) -> DataFrame:
        return DataFrame(
            BowDamageTrial.objects.filter(**self.queryset_filter).values()
        )

    def _fit(self) -> CachedPredictor:
        df = self._prepare_dataframe()
        if df.empty:
            return {"predictor": None, "summary": "No Data"}

        predictor = ols(formula=self.formula, data=df).fit()

        return {
            "predictor": predictor,
            "summary": predictor.summary().as_html(),
        }

    @property
    def predictor(self) -> Optional[RegressionResultsWrapper]:
        return self._instance_cache[self.id]["predictor"]

    @property
    def summary(self) -> str:
        return self._instance_cache[self.id]["summary"]

    def predict(self, *args, **kwargs) -> list[float]:
        """
        Wrapper around `RegressionResultsWrapper.predict` which accepts a dict
         of observations keyed by regressor name like `{"feature": [...]}` and
         returns a list of predicted values for the observations.
        """
        if not self.predictor:
            raise RuntimeError("No model available for prediction (no data?)")
        return list(self.predictor.predict(*args, **kwargs))

    def __str__(self) -> str:
        return f"{self.formula} for {self.queryset_filter}"
