from datetime import datetime
from typing import Optional, Dict, List

from pydantic import BaseModel


class ConfigBase(BaseModel):
    gpt: str
    max_tokens: int 
    temperature: float


class SystemBase(BaseModel):
    gender: str
    language: str
    character: str
    other_setting: Optional[str]


class MessageBase(BaseModel):
    role: str
    content: str
    timestamp: datetime


# 新規にChatを作成する際のリクエスト
class ChatRequestBase(BaseModel):
    content: str
    role: str
    config: ConfigBase
    system: SystemBase


# 既存のChatに対して追加質問するリクエスト
class AddChatRequestBase(BaseModel):
    content: str


# Chat GPT回答のレスポンス
class ChatGPTResponseBase(BaseModel):
    message: Dict[str, str]


