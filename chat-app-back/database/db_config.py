import traceback

from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import SQLAlchemyError

from routes.shemas import ConfigResponse
from database.models import DbConfig, DbGPT

def get_config(chat_id: int, db :Session) -> ConfigResponse:
    """対象のChat IDのConfigを取得する

    Args:
        chat_id (int): 対象のChat ID
        db (Session): 接続するデータベース

    Raises:
        HTTPException HTTP_404_NOT_FOUND: 選択したIDが見つからない場合
        HTTPException HTTP_500_INTERNAL_SERVER_ERROR: 処理中にエラーが発生した場合

    Returns:
        config (ConfigResponse): Configデータ
    """
    try:
        config_db = db.query(DbConfig).filter(DbConfig.chat_id == chat_id).first()

        if config_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Config (chat id {id}) is not found in DB.")

        config = ConfigResponse(
            id = config_db.id,
            chat_id = config_db.chat_id,
            gpt = db.query(DbGPT).filter(DbGPT.id == config_db.gpt_id).first().gpt,
            max_tokens =  config_db.max_tokens,
            temperature =  config_db.temperature,
        )
        return config

    except SQLAlchemyError as e:
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Fatal for getting chat id {id} from DB.")
