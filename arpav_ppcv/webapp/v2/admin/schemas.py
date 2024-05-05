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
