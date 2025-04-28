import asyncio

from prisma import Prisma


async def main():
    prisma = Prisma()
    await prisma.connect()

    # すでにデータがあったら一旦全部消してもいい（テスト用なら）
    await prisma.todo.delete_many()

    # 11件登録
    for i in range(1, 12):
        await prisma.todo.create(
            data={
                "title": f"Todo {i}",
                "done": False,
            }
        )

    await prisma.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
