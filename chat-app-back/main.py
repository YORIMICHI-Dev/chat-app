from pathlib import Path

from fastapi import FastAPI

from routes import chat
from database import models
from database.database import engine, SessionLocal

app = FastAPI()
app.include_router(chat.router)

# database models.pyにて定義したDB作成
@app.on_event("startup")
def startup_event():
    if not Path("chat_app.db").exists():
        models.Base.metadata.create_all(engine)
        with SessionLocal() as session:
            models.initialize(session)


@app.get("/")
def root():
    return {"message": "root"}


