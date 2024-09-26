import pydantic


class StartMessage(pydantic.BaseModel):
    text: str
    photo: str | None = None
    video: str | None = None
