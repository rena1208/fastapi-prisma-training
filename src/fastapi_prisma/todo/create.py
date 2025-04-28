from fastapi import FastAPI
from pydantic import BaseModel
from prisma import Prisma
from contextlib import asynccontextmanager

prisma = Prisma()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await prisma.connect()
    yield
    await prisma.disconnect()

app = FastAPI(lifespan=lifespan)

# リクエスト用のモデル
class TodoCreateRequest(BaseModel):
    title: str

# レスポンス用のモデル
class TodoResponse(BaseModel):
    id: int
    title: str
    done: bool

@app.post("/todos", response_model=TodoResponse)
async def create_todo(todo: TodoCreateRequest):
    created = await prisma.todo.create(
        data={
            "title": todo.title,
            "done": False,  # 初期状態ではdone=False
        }
    )
    return created