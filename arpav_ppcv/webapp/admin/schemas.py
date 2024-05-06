import uuid

import sqlmodel


class ConfigurationParameterValueRead(sqlmodel.SQLModel):
    id: uuid.UUID
    name: str
    description: str


class ConfigurationParameterRead(sqlmodel.SQLModel):
    id: uuid.UUID
    name: str
    description: str
    allowed_values: list[ConfigurationParameterValueRead]


class ConfigurationParameterPossibleValueRead(sqlmodel.SQLModel):
    configuration_parameter_value_id: uuid.UUID
    configuration_parameter_value_name: str


class CoverageConfigurationRead(sqlmodel.SQLModel):
    id: uuid.UUID
    name: str
    coverage_id_pattern: str
    thredds_url_pattern: str
    unit: str
    palette: str
    color_scale_min: float
    color_scale_max: float
    possible_values: list[ConfigurationParameterPossibleValueRead]
