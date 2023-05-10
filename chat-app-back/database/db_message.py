import traceback
from datetime import datetime
from typing import List, Dict

from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session

from routes.shemas import MessageBase
from database.models import DbMessage, DbRole

def get_messages(chat_id: int, db :Session) -> List[MessageBase]:
    try:
        messages_db = db.query(DbMessage).filter(DbMessage.chat_id == chat_id).all()

        if messages_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Message (chat id {id}) is not found in DB.")
        print(messages_db)
        past_messages: List[MessageBase] = [
            MessageBase(
                role = db.query(DbRole).filter(DbRole.id == message.role_id).first().role,
                content = message.content,
                timestamp = message.timestamp,
            )
            for message in messages_db
        ]

        return past_messages

    except:
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Fatal for getting chat id {id} from DB.")


def insert_messages(message: MessageBase, db: Session) -> Dict[str, str]:
    try:
        new_message = DbMessage(
            role = None,
            chat_id = None,
            role_id = None,
            content = None,
            timestamp = datetime.now()
        )

        db.add(new_message)
        db.commit()

        message = {"message": "Chat GPT response was inserted into message table."}
        return  message

    except:
        traceback.print_exc()
        db.rollback()
        HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      detail="Fatal for inserting Chat GPT response message into message table.")
    finally:
        db.close()
