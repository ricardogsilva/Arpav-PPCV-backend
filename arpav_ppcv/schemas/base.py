import pydantic
import sqlmodel


class ResourceList(pydantic.BaseModel):
    items: list[sqlmodel.SQLModel]
