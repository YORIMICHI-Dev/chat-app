from pydantic import BaseModel


class ChatBase(BaseModel):
    params: str
    prompt: str

