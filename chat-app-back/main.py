from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import chat
from database import models
from database.database import engine, SessionLocal

app = FastAPI()
app.include_router(chat.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:3000",],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)


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
