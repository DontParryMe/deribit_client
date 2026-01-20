from contextlib import asynccontextmanager

from fastapi import FastAPI

from .api.price_api import PriceAPI
from .db.database import Database


@asynccontextmanager
async def lifespan(app: FastAPI):
    await Database.init_tables()
    yield


app = FastAPI(title="Crypto Price API", lifespan=lifespan)

price_api = PriceAPI()
app.include_router(price_api.router)
