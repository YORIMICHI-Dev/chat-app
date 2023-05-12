import traceback
from typing import List, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session

from chat.chat_model import ChatAPI, RoleEnum
from chat.system_model import SystemModel
from database import db_chat, db_system, db_config, db_message
from database.database import get_db
from database.models import DbChat
from routes.shemas import ChatRequest, ChatGPTResponse, AddChatRequest, ChatResponse

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)


@router.get(path="/all_chats", response_model=List[ChatResponse])
def get_all_chats(db: Session = Depends(get_db)) -> List[DbChat]:
    """データベースに保存されているすべてのChatを取得する

    Args:
        db (Session, optional): 接続するデータベース Defaults to Depends(get_db).

    Returns:
        message (List[DbChat]): 取得したすべてのChat
    """
    return db_chat.get_all_chats(db=db)


@router.get(path="/get_chat/{id}", response_model=ChatResponse)
def get_all_chat(id: int, db: Session = Depends(get_db)) -> DbChat:
    """対象のChat IDを取得する

    Args:
        id (int): 取得対象のChat ID
        db (Session, optional): 接続するデータベース Defaults to Depends(get_db).

    Returns:
        message (DbChat): 取得したChat
    """
    return db_chat.get_chat(id=id, db=db)


@router.post(path="/create_chat", response_model=ChatGPTResponse)
def create_chat(request: ChatRequest, db: Session = Depends(get_db)) -> ChatGPTResponse:
    """Chatデータと付随するSystemとMessageを新規に作成する

    また、リクエストからChat GPTの返答を取得する

    Args:
        request (ChatRequest): 新規に作成するChatデータおよび質問内容
        db (Session, optional): 接続するデータベース Defaults to Depends(get_db).

    Returns:
        response (ChatGPTResponse): Chat GPTからの返答
    """
    try:
        created_response: Dict[str, int] = db_chat.create_chat(db=db, request=request)

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

        # Chat GPTに渡すメッセージとしてシステム情報と質問内容を登録し返答を取得する
        question = {"role": RoleEnum.user.value, "content": request.content}
        new_messages: List[Dict[str, str]] = [request_system.system, question]
        gpt_response = bot.create_response(messages=new_messages)

        # Chat GPTからのメッセージをmessageデータベースに保存する
        _ = db_message.insert_messages(
            messages=[gpt_response["message"]], chat_id=created_response["new_chat_id"], db=db
        )

        return gpt_response

    except:
        traceback.print_exc()
        # 処理中にエラーが発生した場合はdb_chat.create_chatのコミットをロールバックする
        db.rollback()
    
    finally:
        db.close()


@router.post(path="/add_chat/{chat_id}", response_model=ChatGPTResponse)
def add_chat(chat_id: int, request: AddChatRequest, db: Session = Depends(get_db)):
    """対象のChat IDに対して追加で質問する

    Args:
        chat_id (int): 対象のChat ID
        request (AddChatRequestBase): 追加の質問内容
        db (Session, optional): 接続するデータベース Defaults to Depends(get_db).

    Returns:
        response (List[DbChat]): 取得したすべてのChat
    """
    try:
        # 現在のChat IDからSystemとConfigを取得する
        current_chat = db_chat.get_chat(id=chat_id, db=db)
        current_config = db_config.get_config(chat_id=current_chat.id, db=db)
        current_system = db_system.get_system(chat_id=current_chat.id, db=db)

        # Chat GPTに渡すメッセージとしてシステム情報を登録
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

        # Chat GPTに渡す過去のメッセージを取得
        past_messages = db_message.get_messages(chat_id=chat_id, db=db)
        question = {"role": RoleEnum.user.value, "content": request.content}
        new_messages: List[Dict[str, str]] = [request_system.system] + past_messages + [question]

        gpt_response = bot.create_response(messages=new_messages)

        # 質問内容とGPTの返答をmessageデータベースに登録
        _ = db_message.insert_messages(messages=[question, gpt_response["message"]], chat_id=current_chat.id, db=db)

        return gpt_response

    except:
        traceback.print_exc()
        # 処理中にエラーが発生した場合はdb_chat.create_chatのコミットをロールバックする
        db.rollback()
        HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      detail="Fatal for inserting Chat GPT response message into message table.")

    finally:
        db.close()


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

