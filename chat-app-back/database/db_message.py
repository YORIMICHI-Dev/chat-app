import traceback
from datetime import datetime
from typing import List, Dict

from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import SQLAlchemyError

from routes.shemas import MessageResponse
from database.models import DbMessage, DbRole


def get_messages(chat_id: int, db :Session) -> List[Dict[str, str]]:
    """対象のChat IDのMessageのリストを取得しChat GPTが読み込む形式 {"role", "content"}のリストに整形し返す

    Args:
        chat_id (int): 対象のChat ID
        db (Session): 接続するデータベース

    Raises:
        HTTPException HTTP_404_NOT_FOUND: 選択したIDが見つからない場合
        HTTPException HTTP_500_INTERNAL_SERVER_ERROR: 処理中にエラーが発生した場合

    Returns:
        gpt_messages (List[Dict[str, str]]): Chat GPTが読み込む形式のデータリスト
    """
    try:
        messages_db = db.query(DbMessage).filter(DbMessage.chat_id == chat_id).all()

        if messages_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Message (chat id {id}) is not found in DB.")

        # 該当のChat IDの過去メッセージを取得し時系列順に並べる
        past_messages: List[MessageResponse] = [
            MessageResponse(
                id  = message.id,
                chat_id = message.chat_id,
                role = db.query(DbRole).filter(DbRole.id == message.role_id).first().role,
                content = message.content,
                timestamp = message.timestamp,
            )
            for message in messages_db
        ]
        sort_messages = sorted(past_messages, key=lambda message: message.timestamp)

        # Chat GPTが読み込む辞書型{"system": "content"}に整形
        gpt_messages = [{"role": message.role, "content": message.content} for message in sort_messages]

        return gpt_messages
    
    except SQLAlchemyError as e:
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Fatal for getting chat id {id} from DB.")


def insert_messages(messages: List[Dict[str,str]], chat_id: int, db: Session) -> Dict[str, str]:
    try:
        register_messages = [
            DbMessage(
                chat_id = chat_id,
                role_id = db.query(DbRole).filter(DbRole.role == message["role"]).first().id,
                content = message["content"],
                timestamp = datetime.now()
            )
            for message in messages
        ]
        
        for message in register_messages:
            db.add(message)
        db.commit()

        return  

    except SQLAlchemyError as e:
        traceback.print_exc()
        db.rollback()
        HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      detail="Fatal for inserting Chat GPT response message into message table.")
    finally:
        db.close()
