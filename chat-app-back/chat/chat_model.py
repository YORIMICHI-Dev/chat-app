import os
from pathlib import Path
from enum import Enum
from typing import Dict, List, Optional

import openai
from dotenv import load_dotenv
from pydantic import BaseModel, confloat, conint

from chat.system_model import SystemModel

# APIキーの読み込み
env_path = os.path.join(Path(__file__).resolve().parent.parent, ".env")
load_dotenv(env_path)
openai.api_key = os.getenv("OPEN_API_KEY")


class RoleEnum(str, Enum):
    system = "system"
    user = "user"
    assistant = "assistant"


class GPTEnum(str, Enum):
    """Chat GPTで使用可能なモデル名

    Attributes:
        gpt_3_5_turbo: GPT-3.5モデル
        text_davinci_003: GPT-3.5モデル
        code_davinci_002: GPT-3.5モデル
    """
    gpt_3_5_turbo = "gpt-3.5-turbo"
    text_davinci_003 = "text-davinci-003"
    code_davinci_002 = "code-davinci-002"

    @classmethod
    def get_value(cls, name: str) -> str:
        return cls[name].value


class ChatAPI(BaseModel):
    gpt: GPTEnum
    system_model: SystemModel
    max_tokens: conint(gt=0, le=150) = 150
    temperature: confloat(gt=0, le=1.0) = 0.5
    n: int = 1
    stop: Optional[str] = None

    @classmethod
    def chat_factory(cls, gpt_str: str, system_model: SystemModel, max_tokens: int, temperature: float):
        gpt = GPTEnum.get_value(gpt_str)
        return cls(
            gpt=gpt, 
            system_model=system_model, 
            max_tokens=max_tokens, 
            temperature=temperature
        )

    def create_response(self, messages: Dict[str, List[str]]):
        response = openai.ChatCompletion.create(
            model=self.gpt.value,
            messages=messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            n=self.n,
            stop=self.stop,
        )

        return response

