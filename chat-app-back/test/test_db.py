from datetime import datetime
from pprint import pprint

from sqlalchemy.orm.session import Session

from database.database import get_db
from database.models import DbChat, DbMessage, DbSystem

# chat, system, をコミットする
def test_push_db(db: Session):
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

    new_system1 = DbSystem(
        chat_id = 1,
        gender_id = 1,
        language_id = 1,
        character_id = 1,
        other_setting = "The other"
    )

    new_system2 = DbSystem(
        chat_id = 2,
        gender_id = 2,
        language_id = 2,
        character_id = 2,
        other_setting = None,
    )

    db.add(new_system1)
    db.add(new_system2)
    db.commit()


def test_check_db(db: Session):
    chats = db.query(DbChat).all()
    messages = db.query(DbMessage).all()
    systems = db.query(DbSystem).all()

    pprint(chats)
    pprint(messages)
    pprint(systems)


if __name__ == "__main__":
    db = next(get_db())

    if False:
        test_push_db(db)

    if False:
        test_check_db(db)


