from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..prisma_client import prisma

router = APIRouter()

# 削除用のリクエストモデル
class TodoDeleteRequest(BaseModel):
    title: str
    done: bool

# レスポンス用のモデル
class TodoResponse(BaseModel):
    id: int
    title: str
    done: bool

@router.delete("/{id}", response_model=TodoResponse)
async def delete_todo(id: int):
    existing = await prisma.todo.find_unique(where={"id": id})
    if not existing:
        raise HTTPException(status_code=404, detail="todoが見つかりません")

    deleted = await prisma.todo.delete(
        where={"id": id}
    )
    return deleted