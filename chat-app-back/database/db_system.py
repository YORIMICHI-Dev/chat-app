import traceback

from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session

from routes.shemas import SystemBase
from database.models import DbSystem, DbGender, DbLanguage, DbCharacter

def get_system(chat_id: int, db :Session) -> SystemBase:
    """対象のChat IDのSystemを取得する

    Args:
        chat_id (int): 対象のChat ID
        db (Session): 接続するデータベース

    Raises:
        HTTPException HTTP_404_NOT_FOUND: 選択したIDが見つからない場合
        HTTPException HTTP_500_INTERNAL_SERVER_ERROR: 処理中にエラーが発生した場合

    Returns:
        config (ConfigBase): Systemデータ
    """
    try:
        system_db = db.query(DbSystem).filter(DbSystem.chat_id == chat_id).first()

        if system_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"System (chat id {id}) is not found in DB.")

        system = SystemBase(
            gender =  db.query(DbGender).filter(DbGender.id == system_db.gender_id).first().gender,
            language = db.query(DbLanguage).filter(DbLanguage.id == system_db.language_id).first().language,
            character =  db.query(DbCharacter).filter(DbCharacter.id == system_db.character_id).first().character,
            other_setting =  system_db.other_setting
        )
        return system

    except:
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Fatal for getting chat id {id} from DB.")
