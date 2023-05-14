from datetime import datetime
from typing import Optional, Dict, List

from pydantic import BaseModel


# 新規にChatを作成する際のリクエスト
class ConfigRequest(BaseModel):
    gpt: str
    max_tokens: int 
    temperature: float


class SystemRequest(BaseModel):
    gender: str
    language: str
    character: str
    other_setting: Optional[str]


class ChatRequest(BaseModel):
    content: str
    role: str
    config: ConfigRequest
    system: SystemRequest


# 既存のChatに対して追加質問するリクエスト
class AddChatRequest(BaseModel):
    content: str


# Chatデータのレスポンス
class ConfigResponse(BaseModel):
    id: int
    chat_id: int
    gpt: str
    max_tokens: int 
    temperature: float


class SystemResponse(BaseModel):
    id: int
    chat_id: int
    gender: str
    language: str
    character: str
    other_setting: Optional[str]


class MessageResponse(BaseModel):
    id: int
    chat_id: int
    role: str
    content: str
    timestamp: datetime

class ChatResponse(BaseModel):
    chat_id: int
    title: str
    timestamp: datetime
    system: SystemResponse
    config: ConfigResponse
    messages: List[MessageResponse]


# 新規Chat作成時のレスポンス
class CreateChatResponse(BaseModel):
    chat_id: int


# 既存Chatへの追加質問時のレスポンス
class AddChatResponse(BaseModel):
    chat_id: int

