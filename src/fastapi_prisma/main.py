from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .prisma_client import prisma
from prisma import errors as prisma_errors

from .todo import create


@asynccontextmanager
async def lifespan(app: FastAPI):
    await prisma.connect()
    yield
    await prisma.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(create.router, prefix="/todos")

class TodoModel(BaseModel):
    id: int
    title: str
    done: bool
    createdAt: datetime
    updatedAt: datetime

@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/todos")
async def get_todos(page: int = 1) -> list[TodoModel]:
    per_page = 10
    try:
        return await prisma.todo.find_many(
            take=per_page,
            skip=(page - 1) * per_page
        )
    except prisma_errors.PrismaError as e:
        print(e)
        raise HTTPException(status_code=400, detail="fetch failed")
