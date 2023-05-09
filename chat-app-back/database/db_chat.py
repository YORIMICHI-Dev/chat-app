from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session

from routes.shemas import ChatRequestBase
from database.models import DbChat, DbMessage, DbSystem, DbRole, DbGender, DbCharacter, DbLanguage


def get_all_chat(db: Session):
    try:
        chat = db.query(DbChat).all()
        return chat
    
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Fatal for getting all chat data from DB.")


def create_chat(db: Session, request: ChatRequestBase):
    try:
        new_chat = DbChat(
            title = request.content,
            timestamp = datetime.now(),
        )
        db.add(new_chat)
        db.commit()
        db.refresh(new_chat)

        new_message = DbMessage(
            chat_id = new_chat.id,
            role_id = db.query(DbRole).filter(DbRole.role == request.config.role).filter(),
            content = request.content,
            timestamp = datetime.now(),
        )
        db.add(new_message)
        db.commit()
        db.refresh(new_message)

        new_system = DbSystem(
            chat_id = new_chat.id,
            gender_id = db.query(DbGender).filter(DbGender.gender == request.system.gender).filter(),
            language_id = db.query(DbLanguage).filter(DbLanguage.role == request.system.language).filter(),
            character_id = db.query(DbCharacter).filter(DbCharacter.role == request.system.character).filter(),
            other_setting = request.system.other_setting,
        )
        db.add(new_system)
        db.commit()
        db.refresh(new_system)

        return {
            "chat": new_chat,
            "message": new_message,
            "system": new_system,
        }

    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Fatal for create new chat data.")
