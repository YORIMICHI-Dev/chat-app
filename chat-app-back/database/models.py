from fastapi import Depends
from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, DateTime

from database.database import Base, get_db
from chat.system_model import GenderEnum, LanguageEnum, CharacterEnum
from chat.chat_model import RoleEnum


class DbChat(Base):
    __tablename__ = "chat"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    system = relationship("DbSystem", back_populates="chat")
    messages = relationship("DbMessage", back_populates="chat")
    timestamp = Column(DateTime, nullable=False)


class DbMessage(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey(column="chat.id", ondelete="CASCADE"))
    role_id = Column(Integer, nullable=False)
    content = Column(String(255), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    chat = relationship("DbChat", back_populates="messages")


class DbRole(Base):
    __tablename__ = "role"
    id = Column(Integer, ForeignKey(column="message.role_id"), primary_key=True, index=True, autoincrement=True)
    role = Column(String(10), nullable=False, unique=True)


class DbSystem(Base):
    __tablename__ = "system"
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey(column="chat.id", ondelete="CASCADE"))
    gender_id = Column(Integer, nullable=False)
    language_id = Column(Integer, nullable=False)
    character_id = Column(Integer, nullable=False)
    other_setting = Column(String(255))
    chat = relationship("DbChat", back_populates="system")


class DbGender(Base):
    __tablename__ = "gender"
    id = Column(Integer, ForeignKey(column="system.gender_id", ondelete="NO ACTION"), primary_key=True, index=True, autoincrement=True)
    gender = Column(String(10), nullable=False, unique=True)


class DbLanguage(Base):
    __tablename__ = "language"
    id = Column(Integer, ForeignKey(column="system.gender_id", ondelete="NO ACTION"), primary_key=True, index=True, autoincrement=True)
    language = Column(String(5), nullable=False, unique=True)


class DbCharacter(Base):
    __tablename__ = "character"
    id = Column(Integer, ForeignKey(column="system.character_id", ondelete="NO ACTION"), primary_key=True, index=True, autoincrement=True)
    character = Column(String(10), nullable=False, unique=True)
    description = Column(String(100), nullable=False, unique=True)


def initialize(db: Session):
    gender_list = [gender.value for gender in GenderEnum]
    for gender in gender_list:
        new_gender = DbGender(
            gender = gender
        )
        db.add(new_gender)
        db.commit()

    language_list = [language.value for language in LanguageEnum]
    for language in language_list:
        new_language = DbLanguage(
            language = language
        )
        db.add(new_language)
        db.commit()

    character_dict = {character.name: character.value for character in CharacterEnum}
    for character, description in character_dict.items():
        new_character = DbCharacter(
            character = character,
            description = description,
        )
        db.add(new_character)
        db.commit()

    role_list = [role.value for role in RoleEnum]
    for role in role_list:
        new_role = DbRole(
            role = role
        )
        db.add(new_role)
        db.commit()
