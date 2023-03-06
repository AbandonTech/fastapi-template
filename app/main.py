from fastapi import Depends, FastAPI
from prisma import Prisma

from app.dependencies import use_logging
from app.middleware import LoggingMiddleware

app = FastAPI()
app.add_middleware(LoggingMiddleware, fastapi=app)

prisma = Prisma(auto_register=True)


@app.get("/")
async def root(logger=Depends(use_logging)):
    logger.info("Handling your request")
    return {"message": "Your app is working!"}


@app.on_event("startup")
async def startup() -> None:
    await prisma.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    if prisma.is_connected():
        await prisma.disconnect()
