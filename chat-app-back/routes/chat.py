from fastapi import APIRouter


router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)


@router.get(path="/all_chat")
def get_all_chat():
    # TODO データベースに格納している過去のチャットを取得する
    return 0


@router.post(path="/create_chat")
def create_chat():
    # TODO 新しいチャットデータをデータベースに作成する
    return 0


@router.put(path="/put_chat")
def put_chat():
    # TODO 既存のチャットデータに追加で質問する
    return 0


@router.delete(path="/delete_chat")
def delete_chat():
    # TODO 既存のチャットデータを削除する
    return 0

