import uuid
from typing import Optional

import sqlalchemy
import sqlmodel


class ConfigurationParameterValue(sqlmodel.SQLModel, table=True):
    __table_args__ = (
        sqlalchemy.ForeignKeyConstraint(
            ["configuration_parameter_id",],
            ["configurationparameter.id",],
            onupdate="CASCADE",
            ondelete="CASCADE",  # i.e. delete param value if its related param gets deleted
        ),
    )
    id: uuid.UUID = sqlmodel.Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )
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
            "order_by": "ConfigurationParameterPossibleValue.configuration_parameter_value_id"
        }
    )


class ConfigurationParameter(sqlmodel.SQLModel, table=True):
    id: uuid.UUID = sqlmodel.Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )
    name: str = sqlmodel.Field(unique=True, index=True)
    description: str

    allowed_values: list[ConfigurationParameterValue] = sqlmodel.Relationship(
        back_populates="configuration_parameter",
        sa_relationship_kwargs={
            "cascade": "all, delete, delete-orphan",
            "passive_deletes": True,
            "order_by": "ConfigurationParameterValue.name",
        }
    )


class ConfigurationParameterValueCreateEmbeddedInConfigurationParameter(
    sqlmodel.SQLModel
):
    name: str
    description: str


class ConfigurationParameterCreate(sqlmodel.SQLModel):
    name: str
    description: str

    allowed_values: list[
        ConfigurationParameterValueCreateEmbeddedInConfigurationParameter
    ]


class ConfigurationParameterValueUpdateEmbeddedInConfigurationParameterEdit(sqlmodel.SQLModel):
    id: Optional[uuid.UUID] = None
    name: Optional[str] = None
    description: Optional[str] = None


class ConfigurationParameterUpdate(sqlmodel.SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None

    allowed_values: list[
        ConfigurationParameterValueUpdateEmbeddedInConfigurationParameterEdit
    ]


class CoverageConfiguration(sqlmodel.SQLModel, table=True):
    """Configuration for NetCDF datasets.

    Can refer to either model forecast data or historical data derived from
    observations.
    """
    id: uuid.UUID = sqlmodel.Field(
        default_factory=uuid.uuid4,
        primary_key=True
    )
    name: str = sqlmodel.Field(unique=True, index=True)
    thredds_url_pattern: str
    unit: str = ""
    palette: str
    color_scale_min: float = 0.0
    color_scale_max: float = 1.0

    possible_values: list["ConfigurationParameterPossibleValue"] = sqlmodel.Relationship(
        back_populates="coverage_configuration",
        sa_relationship_kwargs={
            "cascade": "all, delete, delete-orphan",
            "passive_deletes": True,
        }
    )


class CoverageConfigurationCreate(sqlmodel.SQLModel):
    name: str
    thredds_url_pattern: str
    unit: str
    palette: str
    color_scale_min: float
    color_scale_max: float
    possible_values: list["ConfigurationParameterPossibleValueCreate"]


class CoverageConfigurationUpdate(sqlmodel.SQLModel):
    name: Optional[str] = None
    thredds_url_pattern: Optional[str] = None
    unit: Optional[str] = None
    palette: Optional[str] = None
    color_scale_min: Optional[float] = None
    color_scale_max: Optional[float] = None
    possible_values: list["ConfigurationParameterPossibleValueUpdate"]


class ConfigurationParameterPossibleValue(sqlmodel.SQLModel, table=True):
    """Possible values for a parameter of a coverage configuration.

    This model mediates an association table that governs a many-to-many relationship
    between a coverage configuration and a configuration parameter value."""
    __table_args__ = (
        sqlalchemy.ForeignKeyConstraint(
            ["coverage_configuration_id",],
            ["coverageconfiguration.id",],
            onupdate="CASCADE",
            ondelete="CASCADE",  # i.e. delete all possible values if the related coverage configuration gets deleted
        ),
        sqlalchemy.ForeignKeyConstraint(
            ["configuration_parameter_value_id", ],
            ["configurationparametervalue.id", ],
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
        back_populates="possible_values")
    configuration_parameter_value: ConfigurationParameterValue = sqlmodel.Relationship(
        back_populates="used_in_configurations")


class ConfigurationParameterPossibleValueCreate(sqlmodel.SQLModel):
    configuration_parameter_value_id: uuid.UUID


class ConfigurationParameterPossibleValueUpdate(sqlmodel.SQLModel):
    configuration_parameter_value_id: uuid.UUID

# def _get_subclasses(cls):
#     for subclass in cls.__subclasses__():
#         yield from _get_subclasses(subclass)
#         yield subclass
#
#
# _models_dict = {cls.__name__: cls for cls in _get_subclasses(sqlmodel.SQLModel)}
#
# for cls in _models_dict.values():
#     cls.model_rebuild(_types_namespace=_models_dict)
