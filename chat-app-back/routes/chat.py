from typing import Dict, Union

from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from chat.chat_model import ChatAPI
from chat.system_model import SystemModel
from database import db_chat
from database.database import get_db
from database.models import DbChat, DbMessage, DbSystem, DbRole, DbGender, DbCharacter, DbLanguage
from routes.shemas import ChatRequestBase

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)


@router.get(path="/all_chat", response_model=None)
def get_all_chat(db: Session = Depends(get_db)):
    return db_chat.get_all_chat(db=db)


@router.post(path="/create_chat", response_model=None)
def create_chat(request: ChatRequestBase, db: Session = Depends(get_db)):
    # TODO 新しいチャットデータをデータベースに作成する
    create_response: Dict[str, Union[DbChat, DbMessage, DbSystem]] = db_chat.create_chat(db=db, request=request)

    # リクエストされたシステム情報をもとにChat GPTが返答する
    request_system = SystemModel.system_factory(
        gender_str=request.system.gender,
        language_str=request.system.language,
        character_str=request.system.character,
        other_setting=request.system.other_setting,
    )
    bot = ChatAPI.chat_factory(
        model_name=request.config.model, 
        system_settings=request_system, 
        max_tokens=request.config.max_tokens, 
        temperature=request
    )

    # Chat GPTに渡すメッセージとしてシステム情報と質問内容を登録
    question = {"role": "user", "content": request.content}
    messages: Dict[str, str] = dict(**request_system.system, **question)

    return bot.create_response(messges=messages)


@router.post(path="/add_chat/{chat_id}", response_model=None)
def add_chat(chat_id: int, request: ChatRequestBase, db: Session = Depends(get_db)):
    # TODO 既存のチャットデータに追加で質問する
    bot = ChatAPI(**request.config.dict())

    # test
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
    ]
    return bot.create_response(messages=messages)


@router.delete(path="/delete_chat", response_model=None)
def delete_chat():
    # TODO 既存のチャットデータを削除する
    return 0

