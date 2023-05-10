import traceback
from typing import List, Dict, Union

from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from chat.chat_model import ChatAPI, RoleEnum
from chat.system_model import SystemModel
from database import db_chat, db_system, db_config, db_message
from database.database import get_db
from database.models import DbChat, DbConfig, DbMessage, DbSystem
from routes.shemas import ChatRequestBase, ChatGPTResponseBase, AddChatRequestBase

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)


@router.get(path="/all_chats", response_model=None)
def get_all_chats(db: Session = Depends(get_db)) -> List[DbChat]:
    """データベースに保存されているすべてのChatを取得する

    Args:
        db (Session, optional): 接続するデータベース Defaults to Depends(get_db).

    Returns:
        message (List[DbChat]): 取得したすべてのChat
    """
    return db_chat.get_all_chats(db=db)


@router.get(path="/get_chat/{id}", response_model=None)
def get_all_chat(id: int, db: Session = Depends(get_db)) -> DbChat:
    """対象のChat IDを取得する

    Args:
        id (int): 取得対象のChat ID
        db (Session, optional): 接続するデータベース Defaults to Depends(get_db).

    Returns:
        message (DbChat): 取得したChat
    """
    return db_chat.get_chat(id=id, db=db)


@router.post(path="/create_chat", response_model=ChatGPTResponseBase)
def create_chat(request: ChatRequestBase, db: Session = Depends(get_db)) -> ChatGPTResponseBase:
    """Chatデータと付随するSystemとMessageを新規に作成する

    また、リクエストからChat GPTの返答を取得する

    Args:
        request (ChatRequestBase): 新規に作成するChatデータおよび質問内容
        db (Session, optional): 接続するデータベース Defaults to Depends(get_db).

    Returns:
        message (ChatGPTResponseBase): Chat GPTからの返答
    """
    try:
        create_response: Dict[str, Union[DbChat, DbConfig, DbSystem, DbMessage]] = db_chat.create_chat(db=db, request=request)

        # リクエストされたシステム情報をもとにChat GPTが返答する
        request_system = SystemModel.system_factory(
            gender_str=request.system.gender,
            language_str=request.system.language,
            character_str=request.system.character,
            other_setting=request.system.other_setting,
        )
        bot = ChatAPI.chat_factory(
            gpt_str=request.config.gpt, 
            system_model=request_system, 
            max_tokens=request.config.max_tokens, 
            temperature=request.config.temperature,
        )

        # Chat GPTに渡すメッセージとしてシステム情報と質問内容を登録
        question = {"role": RoleEnum.user.value, "content": request.content}
        new_messages: List[Dict[str, str]] = [request_system.system, question]

        response = bot.create_response(messages=new_messages)
        # TODO responseをDbMessageに追加する処理
        return response

    except:
        traceback.print_exc()
        # 処理中にエラーが発生した場合はdb_chat.create_chatのコミットをロールバックする
        db.rollback()
    
    finally:
        db.close()


@router.post(path="/add_chat/{chat_id}", response_model=ChatGPTResponseBase)
def add_chat(chat_id: int, request: AddChatRequestBase, db: Session = Depends(get_db)):
    # 現在のChat IDからSystemと今までのMessageを取得する
    current_chat = db_chat.get_chat(id=chat_id, db=db)
    current_config = db_config.get_config(chat_id=current_chat.id, db=db)
    current_system = db_system.get_system(chat_id=current_chat.id, db=db)

    # リクエストされたシステム情報をもとにChat GPTが返答する
    request_system = SystemModel.system_factory(
        gender_str=current_system.gender,
        language_str=current_system.language,
        character_str=current_system.character,
        other_setting=current_system.other_setting,
    )
    bot = ChatAPI.chat_factory(
        gpt_str=current_config.gpt, 
        system_model=request_system, 
        max_tokens=current_config.max_tokens, 
        temperature=current_config.temperature,
    )

    # Chat GPTに渡すメッセージとしてシステム情報と質問内容を登録
    past_messages = db_message.get_messages(chat_id=chat_id, db=db)
    print(past_messages)
    raise Exception
    question = {"role": RoleEnum.user.value, "content": request.content}
    new_messages: List[Dict[str, str]] = [request_system.system, question]

    return bot.create_response(messages=messages)



@router.delete(path="/delete_chat", response_model=None)
def delete_chat(id: int, db:Session = Depends(get_db)) -> Dict[str, str]:
    """対象のChat IDを削除する

    Args:
        id (int): 削除対象のChat ID
        db (Session, optional): 接続するデータベース Defaults to Depends(get_db).

    Returns:
        message (Dict[str, str]): 削除完了のメッセージ
    """
    return db_chat.delete_chat(id=id, db=db)

