from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Float

from database.database import Base
from chat.system_model import GenderEnum, LanguageEnum, CharacterEnum
from chat.chat_model import RoleEnum, GPTEnum


class DbChat(Base):
    __tablename__ = "chat"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    config = relationship("DbConfig", back_populates="chat")
    system = relationship("DbSystem", back_populates="chat")
    messages = relationship("DbMessage", back_populates="chat")
    timestamp = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<DbChat(id={self.id}, title={self.title}, system={self.system}, messages={self.messages}, timestamp={self.timestamp})>"


class DbConfig(Base):
    __tablename__ = "config"
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey(column="chat.id", ondelete="CASCADE"))
    gpt_id = Column(Integer, nullable=False)
    max_tokens = Column(Integer, nullable=False)
    temperature = Column(Float, nullable=False)
    chat = relationship("DbChat", back_populates="config")

    def __repr__(self):
        return f"<DbConfig(id={self.id}, chat_id={self.chat_id}, gpt_id={self.gpt_id}, max_tokens={self.max_tokens}, temperature={self.temperature})>"


class DbGPT(Base):
    __tablename__ = "gpt"
    id = Column(Integer, ForeignKey(column="config.gpt_id"), primary_key=True, index=True, autoincrement=True)
    gpt = Column(String(20), nullable=False, unique=True)

    def __repr__(self):
        return f"<DbGPT(id={self.id}, gpt={self.gpt}>"


class DbSystem(Base):
    __tablename__ = "system"
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey(column="chat.id", ondelete="CASCADE"))
    gender_id = Column(Integer, nullable=False)
    language_id = Column(Integer, nullable=False)
    character_id = Column(Integer, nullable=False)
    other_setting = Column(String(255))
    chat = relationship("DbChat", back_populates="system")

    def __repr__(self):
        return f"<DbSystem(id={self.id}, chat_id={self.chat_id}, gender_id={self.gender_id}, language_id={self.language_id}, character_id={self.character_id}, other_setting={self.other_setting})>"


class DbGender(Base):
    __tablename__ = "gender"
    id = Column(Integer, ForeignKey(column="system.gender_id", ondelete="NO ACTION"), primary_key=True, index=True, autoincrement=True)
    gender = Column(String(10), nullable=False, unique=True)

    def __repr__(self):
        return f"<DbRole(id={self.id}, gender={self.gender}>"


class DbLanguage(Base):
    __tablename__ = "language"
    id = Column(Integer, ForeignKey(column="system.gender_id", ondelete="NO ACTION"), primary_key=True, index=True, autoincrement=True)
    language = Column(String(5), nullable=False, unique=True)

    def __repr__(self):
        return f"<DbRole(id={self.id}, language={self.language}>"


class DbCharacter(Base):
    __tablename__ = "character"
    id = Column(Integer, ForeignKey(column="system.character_id", ondelete="NO ACTION"), primary_key=True, index=True, autoincrement=True)
    character = Column(String(10), nullable=False, unique=True)
    description = Column(String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"<DbRole(id={self.id}, character={self.character}, description={self.description}>"


class DbMessage(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey(column="chat.id", ondelete="CASCADE"))
    role_id = Column(Integer, nullable=False)
    content = Column(String(255), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    chat = relationship("DbChat", back_populates="messages")

    def __repr__(self):
        return f"<DbMessage(id={self.id}, chat_id={self.chat_id}, role_id={self.role_id}, content={self.content}, timestamp={self.timestamp})>"


class DbRole(Base):
    __tablename__ = "role"
    id = Column(Integer, ForeignKey(column="message.role_id"), primary_key=True, index=True, autoincrement=True)
    role = Column(String(10), nullable=False, unique=True)

    def __repr__(self):
        return f"<DbRole(id={self.id}, role={self.role}>"


def initialize(db: Session) -> None:
    """データベース新規作成時にConfig(gpt), System(gender, language, character), Message(role)テーブルに値を入れる

    Args:
        db (Session): 接続するデータベース
    """
    gpt_list = [gpt.name for gpt in GPTEnum]
    for gpt in gpt_list:
        new_gpt = DbGPT(
            gpt = gpt
        )
        db.add(new_gpt)

    gender_list = [gender.name for gender in GenderEnum]
    for gender in gender_list:
        new_gender = DbGender(
            gender = gender
        )
        db.add(new_gender)

    language_list = [language.name for language in LanguageEnum]
    for language in language_list:
        new_language = DbLanguage(
            language = language
        )
        db.add(new_language)

    character_dict = {character.name: character.value for character in CharacterEnum}
    for character, description in character_dict.items():
        new_character = DbCharacter(
            character = character,
            description = description,
        )
        db.add(new_character)

    role_list = [role.name for role in RoleEnum]
    for role in role_list:
        new_role = DbRole(
            role = role
        )
        db.add(new_role)
        db.commit()
