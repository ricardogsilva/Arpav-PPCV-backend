import enum
import typing
import typing_extensions

import babel
import pydantic
import sqlmodel

from ..config import get_translations


class Translatable(typing.Protocol):
    def get_display_name(self, locale: babel.Locale) -> str:
        ...


class Season(enum.Enum):
    WINTER = "WINTER"
    SPRING = "SPRING"
    SUMMER = "SUMMER"
    AUTUMN = "AUTUMN"

    def get_display_name(self, locale: babel.Locale) -> str:
        translations = get_translations(locale)
        _ = translations.gettext
        return {
            self.WINTER.name: _("winter"),
            self.SPRING.name: _("spring"),
            self.SUMMER.name: _("summer"),
            self.AUTUMN.name: _("autumn"),
        }[self.name]


class ObservationDataSmoothingStrategy(enum.Enum):
    NO_SMOOTHING = "NO_SMOOTHING"
    MOVING_AVERAGE_5_YEARS = "MOVING_AVERAGE_5_YEARS"

    def get_display_name(self, locale: babel.Locale) -> str:
        translations = get_translations(locale)
        _ = translations.gettext
        return {
            self.NO_SMOOTHING.name: _("no processing"),
            self.MOVING_AVERAGE_5_YEARS.name: _("centered 5-year moving average"),
        }[self.name]


UNCERTAINTY_TIME_SERIES_PATTERN = "**UNCERTAINTY**"
RELATED_TIME_SERIES_PATTERN = "**RELATED**"


class ObservationAggregationType(str, enum.Enum):
    MONTHLY = "MONTHLY"
    SEASONAL = "SEASONAL"
    YEARLY = "YEARLY"

    def get_display_name(self, locale: babel.Locale) -> str:
        translations = get_translations(locale)
        _ = translations.gettext
        return {
            self.MONTHLY.name: _("monthly"),
            self.SEASONAL.name: _("seasonal"),
            self.YEARLY.name: _("yearly"),
        }[self.name]


class CoverageDataSmoothingStrategy(enum.Enum):
    NO_SMOOTHING = "NO_SMOOTHING"
    LOESS_SMOOTHING = "LOESS_SMOOTHING"
    MOVING_AVERAGE_11_YEARS = "MOVING_AVERAGE_11_YEARS"

    def get_display_name(self, locale: babel.Locale) -> str:
        translations = get_translations(locale)
        _ = translations.gettext
        return {
            self.NO_SMOOTHING.name: _("no processing"),
            self.LOESS_SMOOTHING.name: _("LOESS"),
            self.MOVING_AVERAGE_11_YEARS.name: _("centered 11-year moving average"),
        }[self.name]


class MannKendallParameters(pydantic.BaseModel):
    start_year: int | None = None
    end_year: int | None = None

    @pydantic.model_validator(mode="after")
    def check_year_span_is_valid(self) -> typing_extensions.Self:
        if self.start_year is not None and self.end_year is not None:
            if self.end_year - self.start_year < 27:
                raise ValueError(
                    "Mann-Kendall start and end years must span 27 years or more"
                )
        return self


class ResourceList(pydantic.BaseModel):
    items: list[sqlmodel.SQLModel]
