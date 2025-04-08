import pydantic


class ButtonMessage(pydantic.BaseModel):
    type: str
    name: str
    url: str | None = None
    callback_data: str | None = None


class StartMessage(pydantic.BaseModel):
    type: str
    text: str
    photo: str | None = None
    video: str | None = None
    buttons: list[ButtonMessage] | None = None
