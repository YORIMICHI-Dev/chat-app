import traceback
from datetime import datetime
from typing import Dict, List, Union

from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session

from routes.shemas import ChatRequestBase
from chat.chat_model import RoleEnum
from database.models import DbChat, DbConfig, DbMessage, DbSystem, DbRole, DbGPT, DbGender, DbCharacter, DbLanguage


def get_all_chats(db: Session) -> List[DbChat]:
    """データベース保存しているすべてのChatデータを取得する

    Args:
        db (Session): 接続するデータベース

    Raises:
        HTTPException HTTP_404_NOT_FOUND: Chatデータが見つからなかった場合
        HTTPException HTTP_500_INTERNAL_SERVER_ERROR: 処理中にエラーが発生した場合

    Returns:
        chats (List[DbChat]): すべてのChatデータ
    """
    try:
        chats = db.query(DbChat).all()

        if chats is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Chats were not found in DB.")

        return chats

    except:
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Fatal for getting all chats from DB.")


def get_chat(id: int, db: Session) -> DbChat:
    """特定IDのChatデータを取得する

    Args:
        id (int): 対象のChat ID
        db (Session): 接続するデータベース

    Raises:
        HTTPException HTTP_404_NOT_FOUND: Chatデータが見つからなかった場合
        HTTPException HTTP_500_INTERNAL_SERVER_ERROR: 処理中にエラーが発生した場合

    Returns:
        chat (DbChat): 特定IDのChatデータ
    """
    try:
        chat = db.query(DbChat).filter(DbChat.id == id).first()

        if chat is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Chat id {id} is not found in DB.")

        return chat

    except:
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Fatal for getting chat id {id} from DB.")


def create_chat(db: Session, request: ChatRequestBase) -> Dict[str, Union[DbChat, DbConfig, DbSystem, DbMessage]]:
    """新規にChatデータを作成する。また、Chatに関するSystemおよびMessageも作成しコミットする

    Args:
        id (int): 削除対象のChat ID
        request (ChatRequestBase): _description_

    Raises:
        HTTPException HTTP_500_INTERNAL_SERVER_ERROR: 処理中にエラーが発生した場合

    Returns:
        message (Dict[str, str]): 削除完了のメッセージ
    """
    try:
        new_chat = DbChat(
            title = request.content,
            timestamp = datetime.now(),
        )
        db.add(new_chat)
        db.flush()

        new_config = DbConfig(
            chat_id = new_chat.id,
            gpt_id = db.query(DbGPT).filter(DbGPT.gpt == request.config.gpt).first().id,
            max_tokens = request.config.max_tokens,
            temperature = request.config.temperature
        )
        db.add(new_config)

        new_system = DbSystem(
            chat_id = new_chat.id,
            gender_id = db.query(DbGender).filter(DbGender.gender == request.system.gender).first().id,
            language_id = db.query(DbLanguage).filter(DbLanguage.language == request.system.language).first().id,
            character_id = db.query(DbCharacter).filter(DbCharacter.character == request.system.character).first().id,
            other_setting = request.system.other_setting,
        )
        db.add(new_system)

        new_message = DbMessage(
            chat_id = new_chat.id,
            role_id = db.query(DbRole).filter(DbRole.role == request.role).first().id,
            content = request.content,
            timestamp = datetime.now(),
        )
        db.add(new_message)
        db.commit()

        message = {
            "chat": new_chat,
            "config": new_config,
            "system": new_system,
            "message": new_message,
        }

        return message

    except:
        traceback.print_exc()
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Fatal for creating new chat data.")

    finally:
        db.close()


def delete_chat(id:int, db: Session):
    """対象のChat IDをデータベースから削除する

    Args:
        id (int): 削除対象のChat ID
        db (Session): 接続するデータベース

    Raises:
        HTTPException HTTP_400_BAD_REQUEST: 選択したIDが見つからない場合
        HTTPException HTTP_500_INTERNAL_SERVER_ERROR: 処理中にエラーが発生した場合

    Returns:
        message (Dict[str, str]): 削除完了のメッセージ
    """
    try:
        chat = db.query(DbChat).filter(DbChat.id == id).first()

        if chat is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Chat id {id} is not found in DB.")
        db.delete(chat)

        message = {"message": f"chat id {id} was deleted."}
        return message
    
    except:
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Chat id {id} is not for create new chat data.")
