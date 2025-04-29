from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..prisma_client import prisma

router = APIRouter()

# 更新用のリクエストモデル
class TodoUpdateRequest(BaseModel):
    title: str 
    done: bool

# レスポンス用のモデル
class TodoResponse(BaseModel):
    id: int
    title: str
    done: bool

@router.patch("/{id}", response_model=TodoResponse)
async def update_todo(id: int, todo: TodoUpdateRequest):
    existing = await prisma.todo.find_unique(where={"id": id})
    if not existing:
        raise HTTPException(status_code=404, detail="todoが見つかりません")

    updated = await prisma.todo.update(
        where={"id": id},
        data={
            "title": todo.title,
            "done": todo.done,
        }
    )
    return updated