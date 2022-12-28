from fastapi import FastAPI
from prisma import Prisma

app = FastAPI()

prisma = Prisma(auto_register=True)


@app.get("/")
async def root():
    return {"message": "Your app is working!"}


@app.on_event("startup")
async def startup() -> None:
    await prisma.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    if prisma.is_connected():
        await prisma.disconnect()
