from typing import Optional

from pydantic import BaseModel


class ConfigBase(BaseModel):
    model: str
    role: str
    max_tokens: int 
    temperature: float


class SystemBase(BaseModel):
    gender: str
    language: str
    character: str
    other_setting: Optional[str]


class ChatRequestBase(BaseModel):
    content: str
    config: ConfigBase
    system: SystemBase
