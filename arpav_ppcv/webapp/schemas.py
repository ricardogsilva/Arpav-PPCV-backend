import pydantic


class AppInformation(pydantic.BaseModel):
    version: str
    git_commit: str
