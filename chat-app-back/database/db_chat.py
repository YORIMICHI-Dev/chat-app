import traceback
from datetime import datetime
from typing import Dict, List

from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import SQLAlchemyError

from routes.shemas import ChatRequest, ChatResponse, SystemResponse, ConfigResponse, MessageResponse
from database.models import DbChat, DbConfig, DbMessage, DbSystem, DbRole, DbGPT, DbGender, DbCharacter, DbLanguage


def get_all_chats(db: Session) -> List[ChatResponse]:
    """データベース保存しているすべてのChatデータを取得する

    Args:
        db (Session): 接続するデータベース

    Raises:
        HTTPException HTTP_404_NOT_FOUND: Chatデータが見つからなかった場合
        HTTPException HTTP_500_INTERNAL_SERVER_ERROR: 処理中にエラーが発生した場合

    Returns:
        chats (List[ChatResponse]): すべてのChatデータ
    """
    try:
        chats = db.query(DbChat).all()

        if chats is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Chats were not found in DB.")

        # レスポンス形式をList[ChatResponse]に変更
        chats_response: List[ChatResponse] = []
        for chat in chats:
            config = ConfigResponse(
                id = chat.config.id,
                chat_id = chat.id,
                gpt = db.query(DbGPT).filter(DbGPT.id == chat.config.gpt_id).first().gpt,
                max_tokens = chat.config.max_tokens,
                temperature = chat.config.temperature
            )

            system = SystemResponse(
                id = chat.system.id,
                chat_id = chat.id,
                gender = db.query(DbGender).filter(DbGender.id == chat.system.gender_id).first().gender,
                language = db.query(DbLanguage).filter(DbLanguage.id == chat.system.language_id).first().language,
                character = db.query(DbCharacter).filter(DbCharacter.id == chat.system.character_id).first().character,
                other_setting = chat.system.other_setting,
            )

            messages = [
                MessageResponse(
                    id = message.id,
                    chat_id =chat.id,
                    role = db.query(DbRole).filter(DbRole.id == message.role_id).first().role,
                    content = message.content,
                    timestamp = message.timestamp
                )
                for message in chat.messages
            ]

            chat_response = ChatResponse(
                chat_id = chat.id,
                title = chat.title,
                timestamp = chat.timestamp,
                config = config,
                system = system,
                messages = messages,
            )
            chats_response.append(chat_response)

        return chats_response

    except SQLAlchemyError as e:
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Fatal for getting all chats from DB. {e}")


def get_chat(id: int, db: Session) -> ChatResponse:
    """特定IDのChatデータを取得する

    Args:
        id (int): 対象のChat ID
        db (Session): 接続するデータベース

    Raises:
        HTTPException HTTP_404_NOT_FOUND: Chatデータが見つからなかった場合
        HTTPException HTTP_500_INTERNAL_SERVER_ERROR: 処理中にエラーが発生した場合

    Returns:
        chat (ChatResponse): 特定IDのChatデータ
    """
    try:
        chat = db.query(DbChat).filter(DbChat.id == id).first()

        if chat is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Chat id {id} is not found in DB.")

        # レスポンス形式をResponseに変更
        config = ConfigResponse(
            id = chat.config.id,
            chat_id = chat.id,
            gpt = db.query(DbGPT).filter(DbGPT.id == chat.config.gpt_id).first().gpt,
            max_tokens = chat.config.max_tokens,
            temperature = chat.config.temperature
        )

        system = SystemResponse(
            id = chat.system.id,
            chat_id = chat.id,
            gender = db.query(DbGender).filter(DbGender.id == chat.system.gender_id).first().gender,
            language = db.query(DbLanguage).filter(DbLanguage.id == chat.system.language_id).first().language,
            character = db.query(DbCharacter).filter(DbCharacter.id == chat.system.character_id).first().character,
            other_setting = chat.system.other_setting,
        )

        messages = [
            MessageResponse(
                id = message.id,
                chat_id =chat.id,
                role = db.query(DbRole).filter(DbRole.id == message.role_id).first().role,
                content = message.content,
                timestamp = message.timestamp
            )
            for message in chat.messages
        ]

        chat_response = ChatResponse(
            chat_id = chat.id,
            title = chat.title,
            timestamp = chat.timestamp,
            config = config,
            system = system,
            messages = messages,
        )


        return chat_response


    except SQLAlchemyError as e:
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Fatal for getting chat id {id} from DB. {e}")


def create_chat(db: Session, request: ChatRequest) -> Dict[str, int]:
    """新規にChatデータを作成する。また、Chatに関するSystemおよびMessageも作成しコミットする

    Args:
        id (int): 削除対象のChat ID
        request (ChatRequest): _description_

    Raises:
        HTTPException HTTP_500_INTERNAL_SERVER_ERROR: 処理中にエラーが発生した場合

    Returns:
        message (Dict[str, int]): 新しく作成したChatのID
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

        message = {"new_chat_id": new_chat.id}

        return message

    except SQLAlchemyError as e:
        traceback.print_exc()
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Fatal for creating new chat data. {e}")

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
        db.commit()

        message = {"message": f"chat id {id} was deleted."}
        return message
    
    except SQLAlchemyError as e:
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Chat id {id} is not for create new chat data. {e}")
