import enum
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


class ObservationAggregationType(enum.Enum):
    MONTHLY = "MONTHLY"
    SEASONAL = "SEASONAL"
    YEARLY = "YEARLY"


class CoverageDataSmoothingStrategy(enum.Enum):
    NO_SMOOTHING = "NO_SMOOTHING"
    LOESS_SMOOTHING = "LOESS_SMOOTHING"
    MOVING_AVERAGE_11_YEARS = "MOVING_AVERAGE_11_YEARS"


class ResourceList(pydantic.BaseModel):
    items: list[sqlmodel.SQLModel]
