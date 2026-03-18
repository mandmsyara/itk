from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.routers.wallets import router as wallet_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("app started")

    yield

    print("app stopped")


app = FastAPI(lifespan=lifespan)

app.include_router(wallet_router)
