import os
from typing import List, Dict, Optional
from enum import Enum

from pydantic import BaseModel
import openai
from dotenv import load_dotenv
load_dotenv()

# APIキーの読み込み
openai.api_key = os.getenv("OPEN_API_KEY")


class ModelEnum(Enum):
    gpt_4_32k = "gpt-4-32k"
    gpt_4 = "gpt-4"
    gpt_3_5_turbo = "gpt-3.5-turbo"


class ChatAPI(BaseModel):
    model: ModelEnum
    system: str = "日本語で回答してください"
    max_tokens: int = 150
    temperature: int = 0.5
    echo: bool = True
    n: int = 1
    stop: Optional[str] = None

    def __post_init__(self):
        pass

    def create_response(self, prompt: Dict[List[str]]):
        response = openai.Completion.create(
            engine = self.model,
            prompt = prompt,
            max_tokens = self.max_tokens,
            temperature = self.temperature,
            echo = self.echo,
            n = self.n,
            stop = self.stop
        )

        return response

