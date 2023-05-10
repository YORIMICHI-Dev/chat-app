import traceback

from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session

from routes.shemas import ConfigBase
from database.models import DbConfig, DbGPT

def get_config(chat_id: int, db :Session) -> ConfigBase:
    try:
        config_db = db.query(DbConfig).filter(DbConfig.chat_id == chat_id).first()

        if config_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Config (chat id {id}) is not found in DB.")

        current_config = ConfigBase(
            gpt = db.query(DbGPT).filter(DbGPT.id == config_db.gpt_id).first().gpt,
            max_tokens =  config_db.max_tokens,
            temperature =  config_db.temperature,
        )
        return current_config

    except:
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Fatal for getting chat id {id} from DB.")
