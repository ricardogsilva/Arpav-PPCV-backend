import dataclasses
import logging
import re
import uuid
from typing import (
    Annotated,
    Optional,
    Final,
    TYPE_CHECKING,
)

import pydantic
import sqlalchemy
import sqlmodel

from .. import exceptions
from . import base

if TYPE_CHECKING:
    from . import observations

logger = logging.getLogger(__name__)
_NAME_PATTERN: Final[str] = r"^[a-z][a-z0-9_]+$"


class ConfigurationParameterValue(sqlmodel.SQLModel, table=True):
    __table_args__ = (
        sqlalchemy.ForeignKeyConstraint(
            [
                "configuration_parameter_id",
            ],
            [
                "configurationparameter.id",
            ],
            onupdate="CASCADE",
            ondelete="CASCADE",  # i.e. delete param value if its related param gets deleted
        ),
    )
    id: uuid.UUID = sqlmodel.Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    description: str
    configuration_parameter_id: uuid.UUID

    configuration_parameter: "ConfigurationParameter" = sqlmodel.Relationship(
        back_populates="allowed_values",
    )
    used_in_configurations: "ConfigurationParameterPossibleValue" = sqlmodel.Relationship(
        back_populates="configuration_parameter_value",
        sa_relationship_kwargs={
            "cascade": "all, delete, delete-orphan",
            "passive_deletes": True,
            "order_by": "ConfigurationParameterPossibleValue.configuration_parameter_value_id",
        },
    )


class ConfigurationParameter(sqlmodel.SQLModel, table=True):
    id: uuid.UUID = sqlmodel.Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = sqlmodel.Field(unique=True, index=True)
    description: str

    allowed_values: list[ConfigurationParameterValue] = sqlmodel.Relationship(
        back_populates="configuration_parameter",
        sa_relationship_kwargs={
            "cascade": "all, delete, delete-orphan",
            "passive_deletes": True,
            "order_by": "ConfigurationParameterValue.name",
        },
    )


class ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
    sqlmodel.SQLModel
):
    name: str
    description: str


class ConfigurationParameterCreate(sqlmodel.SQLModel):
    name: Annotated[
        str,
        pydantic.Field(
            pattern=_NAME_PATTERN,
            help=(
                "Parameter name. Only alphanumeric characters and the underscore are "
                "allowed. Example: my_param"
            ),
        ),
    ]
    # name: str
    description: str

    allowed_values: list[
        ConfigurationParameterValueCreateEmbeddedInConfigurationParameter
    ]


class ConfigurationParameterValueUpdateEmbeddedInConfigurationParameterEdit(
    sqlmodel.SQLModel
):
    id: Optional[uuid.UUID] = None
    name: Optional[str] = None
    description: Optional[str] = None


class ConfigurationParameterUpdate(sqlmodel.SQLModel):
    name: Annotated[Optional[str], pydantic.Field(pattern=_NAME_PATTERN)] = None
    description: Optional[str] = None

    allowed_values: list[
        ConfigurationParameterValueUpdateEmbeddedInConfigurationParameterEdit
    ]


class CoverageConfiguration(sqlmodel.SQLModel, table=True):
    """Configuration for NetCDF datasets.

    Can refer to either model forecast data or historical data derived from
    observations.
    """

    id: uuid.UUID = sqlmodel.Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = sqlmodel.Field(unique=True, index=True)
    display_name_english: Optional[str] = None
    display_name_italian: Optional[str] = None
    netcdf_main_dataset_name: str
    thredds_url_pattern: str
    wms_main_layer_name: Optional[str] = None
    unit: str = ""
    palette: str
    color_scale_min: float = 0.0
    color_scale_max: float = 1.0
    observation_variable_id: Optional[uuid.UUID] = sqlmodel.Field(
        default=None, foreign_key="variable.id"
    )
    observation_variable_aggregation_type: Optional[
        base.ObservationAggregationType
    ] = None
    uncertainty_lower_bounds_coverage_configuration_id: Optional[
        uuid.UUID
    ] = sqlmodel.Field(default=None, foreign_key="coverageconfiguration.id")
    uncertainty_upper_bounds_coverage_configuration_id: Optional[
        uuid.UUID
    ] = sqlmodel.Field(default=None, foreign_key="coverageconfiguration.id")

    possible_values: list[
        "ConfigurationParameterPossibleValue"
    ] = sqlmodel.Relationship(
        back_populates="coverage_configuration",
        sa_relationship_kwargs={
            "cascade": "all, delete, delete-orphan",
            "passive_deletes": True,
        },
    )
    secondary_coverage_configurations: list[
        "RelatedCoverageConfiguration"
    ] = sqlmodel.Relationship(
        back_populates="main_coverage_configuration",
        sa_relationship_kwargs={
            "foreign_keys": (
                "RelatedCoverageConfiguration.main_coverage_configuration_id"
            )
        },
    )
    primary_coverage_configurations: list[
        "RelatedCoverageConfiguration"
    ] = sqlmodel.Relationship(
        back_populates="secondary_coverage_configuration",
        sa_relationship_kwargs={
            "foreign_keys": (
                "RelatedCoverageConfiguration.secondary_coverage_configuration_id"
            )
        },
    )

    related_observation_variable: "observations.Variable" = sqlmodel.Relationship(
        back_populates="related_coverage_configurations"
    )

    uncertainty_lower_bounds_coverage_configuration: Optional[
        "CoverageConfiguration"
    ] = sqlmodel.Relationship(
        back_populates="is_lower_bounds_coverage_configuration_to",
        sa_relationship_kwargs={
            "foreign_keys": "CoverageConfiguration.uncertainty_lower_bounds_coverage_configuration_id",
            "remote_side": "CoverageConfiguration.id",
        },
    )
    is_lower_bounds_coverage_configuration_to: Optional[
        "CoverageConfiguration"
    ] = sqlmodel.Relationship(
        back_populates="uncertainty_lower_bounds_coverage_configuration",
        sa_relationship_kwargs={
            "foreign_keys": "CoverageConfiguration.uncertainty_lower_bounds_coverage_configuration_id",
        },
    )

    uncertainty_upper_bounds_coverage_configuration: Optional[
        "CoverageConfiguration"
    ] = sqlmodel.Relationship(
        back_populates="is_upper_bounds_coverage_configuration_to",
        sa_relationship_kwargs={
            "foreign_keys": "CoverageConfiguration.uncertainty_upper_bounds_coverage_configuration_id",
            "remote_side": "CoverageConfiguration.id",
        },
    )
    is_upper_bounds_coverage_configuration_to: Optional[
        "CoverageConfiguration"
    ] = sqlmodel.Relationship(
        back_populates="uncertainty_upper_bounds_coverage_configuration",
        sa_relationship_kwargs={
            "foreign_keys": "CoverageConfiguration.uncertainty_upper_bounds_coverage_configuration_id",
        },
    )

    @pydantic.computed_field()
    @property
    def coverage_id_pattern(self) -> str:
        id_parts = ["{name}"]
        for match_obj in re.finditer(r"(\{\w+\})", self.thredds_url_pattern):
            id_parts.append(match_obj.group(1))
        return "-".join(id_parts)

    def get_thredds_url_fragment(self, coverage_identifier: str) -> str:
        try:
            used_values = self.retrieve_used_values(coverage_identifier)
        except IndexError as err:
            logger.exception("Could not retrieve used values")
            raise exceptions.InvalidCoverageIdentifierException() from err
        rendered = self.thredds_url_pattern
        for used_value in used_values:
            param_name = (
                used_value.configuration_parameter_value.configuration_parameter.name
            )
            rendered = rendered.replace(
                f"{{{param_name}}}", used_value.configuration_parameter_value.name
            )
        return rendered

    def build_coverage_identifier(
        self, parameters: list[ConfigurationParameterValue]
    ) -> str:
        id_parts = [self.name]
        for match_obj in re.finditer(r"(\{\w+\})", self.coverage_id_pattern):
            param_name = match_obj.group(1)[1:-1]
            if param_name != "name":
                for conf_param_value in parameters:
                    conf_param = conf_param_value.configuration_parameter
                    if conf_param.name == param_name:
                        id_parts.append(conf_param_value.name)
                        break
                else:
                    raise ValueError(f"Invalid param_name {param_name!r}")
            else:
                continue
        return "-".join(id_parts)

    def retrieve_used_values(
        self, coverage_identifier: str
    ) -> list["ConfigurationParameterPossibleValue"]:
        parsed_parameters = self.retrieve_configuration_parameters(coverage_identifier)
        result = []
        for param_name, value in parsed_parameters.items():
            for pv in self.possible_values:
                matches_param_name = (
                    pv.configuration_parameter_value.configuration_parameter.name
                    == param_name
                )
                matches_param_value = pv.configuration_parameter_value.name == value
                if matches_param_name and matches_param_value:
                    result.append(pv)
                    break
            else:
                raise ValueError(f"Invalid parameter/value pair: {(param_name, value)}")
        return result

    def retrieve_configuration_parameters(self, coverage_identifier) -> dict[str, str]:
        pattern_parts = re.finditer(
            r"\{(\w+)\}", self.coverage_id_pattern.partition("-")[-1]
        )
        id_parts = coverage_identifier.split("-")[1:]
        result = {}
        for index, pattern_match_obj in enumerate(pattern_parts):
            id_part = id_parts[index]
            configuration_parameter_name = pattern_match_obj.group(1)
            result[configuration_parameter_name] = id_part
        return result

    def get_seasonal_aggregation_query_filter(
        self, coverage_identifier: str
    ) -> Optional[base.Season]:
        used_values = self.retrieve_used_values(coverage_identifier)
        for used_value in used_values:
            is_temporal_aggregation = (
                used_value.configuration_parameter_value.configuration_parameter.name
                in ("year_period",)
            )
            if is_temporal_aggregation:
                value = used_value.configuration_parameter_value.name.lower()
                if value in ("djf",):
                    result = base.Season.WINTER
                elif value in ("mam",):
                    result = base.Season.SPRING
                elif value in ("jja",):
                    result = base.Season.SUMMER
                elif value in ("son",):
                    result = base.Season.AUTUMN
                break
        else:
            result = None
            logger.warning(
                f"Could not determine appropriate season for coverage "
                f"identifier {coverage_identifier!r}"
            )
        return result


class CoverageConfigurationCreate(sqlmodel.SQLModel):
    name: Annotated[
        str,
        pydantic.Field(
            pattern=_NAME_PATTERN,
            help=(
                "Coverage configuration name. Only alphanumeric characters and the "
                "underscore are allowed. Example: my_name"
            ),
        ),
    ]
    display_name_english: Optional[str] = None
    display_name_italian: Optional[str] = None
    netcdf_main_dataset_name: str
    wms_main_layer_name: Optional[str] = None
    thredds_url_pattern: str
    unit: str
    palette: str
    color_scale_min: float
    color_scale_max: float
    possible_values: list["ConfigurationParameterPossibleValueCreate"]
    observation_variable_id: Optional[uuid.UUID] = None
    observation_variable_aggregation_type: Optional[
        base.ObservationAggregationType
    ] = None
    uncertainty_lower_bounds_coverage_configuration_id: Optional[uuid.UUID] = None
    uncertainty_upper_bounds_coverage_configuration_id: Optional[uuid.UUID] = None
    secondary_coverage_configurations_ids: Annotated[
        Optional[list[uuid.UUID]], pydantic.Field(default_factory=list)
    ]

    @pydantic.field_validator("thredds_url_pattern")
    @classmethod
    def validate_thredds_url_pattern(cls, v: str) -> str:
        for match_obj in re.finditer(r"(\{.*?\})", v):
            if re.match(_NAME_PATTERN, match_obj.group(1)[1:-1]) is None:
                raise ValueError(f"configuration parameter {v!r} has invalid name")
        return v.strip()


class CoverageConfigurationUpdate(sqlmodel.SQLModel):
    name: Annotated[Optional[str], pydantic.Field(pattern=_NAME_PATTERN)] = None
    display_name_english: Optional[str] = None
    display_name_italian: Optional[str] = None
    netcdf_main_dataset_name: Optional[str] = None
    wms_main_layer_name: Optional[str] = None
    thredds_url_pattern: Optional[str] = None
    unit: Optional[str] = None
    palette: Optional[str] = None
    color_scale_min: Optional[float] = None
    color_scale_max: Optional[float] = None
    observation_variable_id: Optional[uuid.UUID] = None
    observation_variable_aggregation_type: Optional[
        base.ObservationAggregationType
    ] = None
    possible_values: list["ConfigurationParameterPossibleValueUpdate"]
    uncertainty_lower_bounds_coverage_configuration_id: Optional[uuid.UUID] = None
    uncertainty_upper_bounds_coverage_configuration_id: Optional[uuid.UUID] = None
    secondary_coverage_configurations_ids: Optional[list[uuid.UUID]] = None

    @pydantic.field_validator("thredds_url_pattern")
    @classmethod
    def validate_thredds_url_pattern(cls, v: str) -> str:
        for match_obj in re.finditer(r"(\{.*?\})", v):
            if re.match(_NAME_PATTERN, match_obj.group(1)[1:-1]) is None:
                raise ValueError(f"configuration parameter {v!r} has invalid name")
        return v.strip()


class RelatedCoverageConfiguration(sqlmodel.SQLModel, table=True):
    """Relates coverage configurations with each other.

    This model mediates an association table that governs a many-to-many relationship
    between a main coverage configuration and other coverage configurations.
    """

    main_coverage_configuration_id: Optional[uuid.UUID] = sqlmodel.Field(
        default=None, primary_key=True, foreign_key="coverageconfiguration.id"
    )
    secondary_coverage_configuration_id: Optional[uuid.UUID] = sqlmodel.Field(
        default=None,
        primary_key=True,
        foreign_key="coverageconfiguration.id",
    )

    main_coverage_configuration: CoverageConfiguration = sqlmodel.Relationship(
        back_populates="secondary_coverage_configurations",
        sa_relationship_kwargs={
            "foreign_keys": "RelatedCoverageConfiguration.main_coverage_configuration_id",
        },
    )
    secondary_coverage_configuration: CoverageConfiguration = sqlmodel.Relationship(
        back_populates="primary_coverage_configurations",
        sa_relationship_kwargs={
            "foreign_keys": "RelatedCoverageConfiguration.secondary_coverage_configuration_id",
        },
    )


class ConfigurationParameterPossibleValue(sqlmodel.SQLModel, table=True):
    """Possible values for a parameter of a coverage configuration.

    This model mediates an association table that governs a many-to-many relationship
    between a coverage configuration and a configuration parameter value."""

    __table_args__ = (
        sqlalchemy.ForeignKeyConstraint(
            [
                "coverage_configuration_id",
            ],
            [
                "coverageconfiguration.id",
            ],
            onupdate="CASCADE",
            ondelete="CASCADE",  # i.e. delete all possible values if the related coverage configuration gets deleted
        ),
        sqlalchemy.ForeignKeyConstraint(
            [
                "configuration_parameter_value_id",
            ],
            [
                "configurationparametervalue.id",
            ],
            onupdate="CASCADE",
            ondelete="CASCADE",  # i.e. delete all possible values if the related conf parameter value gets deleted
        ),
    )

    coverage_configuration_id: Optional[uuid.UUID] = sqlmodel.Field(
        # NOTE: foreign key already defined in __table_args__ in order to be able to
        # specify the ondelete behavior
        default=None,
        primary_key=True,
    )
    configuration_parameter_value_id: Optional[uuid.UUID] = sqlmodel.Field(
        # NOTE: foreign key already defined in __table_args__ in order to be able to
        # specify the ondelete behavior
        default=None,
        primary_key=True,
    )

    coverage_configuration: CoverageConfiguration = sqlmodel.Relationship(
        back_populates="possible_values"
    )
    configuration_parameter_value: ConfigurationParameterValue = sqlmodel.Relationship(
        back_populates="used_in_configurations"
    )


class ConfigurationParameterPossibleValueCreate(sqlmodel.SQLModel):
    configuration_parameter_value_id: uuid.UUID


class ConfigurationParameterPossibleValueUpdate(sqlmodel.SQLModel):
    configuration_parameter_value_id: uuid.UUID


@dataclasses.dataclass
class CoverageInternal:
    configuration: CoverageConfiguration
    identifier: str
