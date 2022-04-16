import re
from abc import abstractmethod
from typing import Optional, Type, TypedDict

from django.core.cache import cache
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.utils.functional import cached_property
from pandas import DataFrame
from statsmodels.base.wrapper import ResultsWrapper
from statsmodels.formula.api import ols


class BowDamageTrial(models.Model):
    """Records data about bow damage dealt to a target dummy over 10 shots"""

    DAMAGE_LOG_RE = re.compile(r"((\d+)(?:\s*)){10}")

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
        help_text="Maximum durability of the bow",
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

    class Meta:
        ordering = ("id",)

    def save(self, *args, **kwargs) -> None:
        # denormalizing bc we'll fit models to these values frequently
        self.mean_damage = sum(map(int, self.damage_log.split())) / 10
        # TODO proper validator
        assert (
            self.durability_current <= self.durability_max
        ), "Invalid durability"
        self.durability_pct = self.durability_current / self.durability_max
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.bow_type} @ {self.range}: {self.mean_damage}"


class CachedDamagePredictor(models.Model):
    """
    Abstract model for a predictor that is fit using the `target_model`
     instances from the DB that match `queryset_filter`. The result is stored
     in the in-memory cache (shared across gunicorn threads, but not across
     containers/EC2 instances). The cache is busted whenever there are new rows
     added for the `target_model`.
    """

    id: int  # stop type complaints for implicit int PK
    queryset_filter = models.JSONField(
        default=dict,
        help_text="The data used to fit the predictive model will be "
        "`target_model.objects.filter(**queryset_filter).values()`",
    )

    @property
    @abstractmethod
    def target_model(self) -> Type[models.Model]:
        """The DB model that contains the data to be used for prediction"""

    class Meta:
        abstract = True
        ordering = ("id",)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if not cache.get(self._cache_key):
            self.update_and_cache()

    def update_and_cache(self) -> None:
        cache.set(self._cache_key, self._fit())

    @cached_property
    def _cache_key(self) -> str:
        # TODO: consider another cache-busting strategy - this approach doesn't
        #  account for possible filters but is a guaranteed index-only query
        last_id = (
            self.target_model.objects.order_by("id")
            .values_list("id", flat=True)
            .last()
        ) or 0
        # if the instance has no id (not saved in DB), we use its location in
        #  memory to identify it
        return f"{self._meta.model_name}:{self.id or id(self)}:{last_id}"

    class CachedValueDict(TypedDict):
        predictor: Optional[ResultsWrapper]
        summary: str

    def _prepare_dataframe(self) -> DataFrame:
        return DataFrame(
            self.target_model.objects.filter(**self.queryset_filter).values()
        )

    @abstractmethod
    def _fit(self) -> CachedValueDict:
        """
        Look up the data from the `target_model`, fit a predictive model, and
         return a dict containing the predictor and a summary of it
        """

    @property
    def predictor(self) -> Optional[ResultsWrapper]:
        return cache.get(self._cache_key)["predictor"]

    @property
    def summary(self) -> str:
        return cache.get(self._cache_key)["summary"]

    def predict(self, *args, **kwargs) -> list[float]:
        """
        Wrapper around `ResultsWrapper.predict`, which accepts a dict of
         observations keyed by regressor name like `{"feature": [...]}` and
         returns a list of predicted values for the observations.
        """
        if not self.predictor:
            raise RuntimeError("No model available for prediction (no data?)")
        return list(self.predictor.predict(*args, **kwargs))

    def save(self, *args, **kwargs) -> None:
        self.update_and_cache()
        super().save(*args, **kwargs)


class CachedOLSPredictor(CachedDamagePredictor):
    """
    Abstract model for a CachedDamagePredictor that uses OLS regression with
     the specified `formula` for prediction
    """

    formula = models.CharField(max_length=500)

    class Meta(CachedDamagePredictor.Meta):
        abstract = True

    def _fit(self) -> CachedDamagePredictor.CachedValueDict:
        df = self._prepare_dataframe()
        if df.empty:
            return {
                "predictor": None,
                "summary": "No Data",
            }

        try:
            predictor: ResultsWrapper = ols(
                formula=self.formula,
                data=df,
            ).fit()
            summary: str = predictor.summary().as_html()
        except Exception as e:
            return {
                "predictor": None,
                "summary": repr(e),
            }

        return {
            "predictor": predictor,
            "summary": summary,
        }

    def __str__(self) -> str:
        return f"{self.formula} for {self.queryset_filter}"


class BowDamagePredictor(CachedOLSPredictor):
    """A CachedOLSPredictor to predict bow damage"""

    target_model = BowDamageTrial
