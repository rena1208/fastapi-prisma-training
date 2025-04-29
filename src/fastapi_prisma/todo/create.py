from fastapi import APIRouter
from pydantic import BaseModel
from ..prisma_client import prisma
# from contextlib import asynccontextmanager

router = APIRouter()

# リクエスト用のモデル
class TodoCreateRequest(BaseModel):
    title: str

# レスポンス用のモデル
class TodoResponse(BaseModel):
    id: int
    title: str
    done: bool

@router.post("/create", response_model=TodoResponse)
async def create_todo(todo: TodoCreateRequest):
    created = await prisma.todo.create(
        data={
            "title": todo.title,
            "done": False,  # 初期状態ではdone=False
        }
    )
    return created