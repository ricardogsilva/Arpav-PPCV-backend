import enum
import typing_extensions

import pydantic
import sqlmodel


class Season(enum.Enum):
    WINTER = "WINTER"
    SPRING = "SPRING"
    SUMMER = "SUMMER"
    AUTUMN = "AUTUMN"


class ObservationDataSmoothingStrategy(enum.Enum):
    NO_SMOOTHING = "NO_SMOOTHING"
    MOVING_AVERAGE_5_YEARS = "MOVING_AVERAGE_5_YEARS"


UNCERTAINTY_TIME_SERIES_PATTERN = "**UNCERTAINTY**"
RELATED_TIME_SERIES_PATTERN = "**RELATED**"


class ObservationAggregationType(str, enum.Enum):
    MONTHLY = "MONTHLY"
    SEASONAL = "SEASONAL"
    YEARLY = "YEARLY"


class CoverageDataSmoothingStrategy(enum.Enum):
    NO_SMOOTHING = "NO_SMOOTHING"
    LOESS_SMOOTHING = "LOESS_SMOOTHING"
    MOVING_AVERAGE_11_YEARS = "MOVING_AVERAGE_11_YEARS"


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
