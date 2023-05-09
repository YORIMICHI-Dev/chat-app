from datetime import datetime

from fastapi import Depends
from sqlalchemy.orm.session import Session

from database.database import get_db
from database.models import DbChat, DbMessage, DbSystem, DbRoll, DbGender, DbLanguage, DbCharacter

# Db初期化時にテスト用データをコミットする
def test_initialize_db(db: Session = Depends(get_db)):
    new_chat1 = DbChat(
        title = "test1",
        timestamp = datetime.now(),
    )

    new_chat2 = DbChat(
        title = "test2",
        timestamp = datetime.now(),
    )

    db.add(new_chat1)
    db.add(new_chat2)
    db.commit()

    new_message1 = DbMessage(
        chat_id = 1,
        role_id = 1,
        content = "test content1",
        timestamp = datetime.now(),
    )

    new_message2 = DbMessage(
        chat_id = 2,
        role_id = 2,
        content = "test content2",
        timestamp = datetime.now(),
    )

    db.add(new_message1)
    db.add(new_message2)
    db.commit()

    new_role1 = DbMessage(
        chat_id = 1,
        role_id = 1,
        content = "test content1",
        timestamp = datetime.now(),
    )