import asyncio
import time

from asgiref.sync import async_to_sync
from celery import Celery

from ..clients.deribit import DeribitClient
from ..core.config import get_settings
from ..db.models import Price
from ..factories.price_factory import PriceServiceFactory

settings = get_settings()

celery_app = Celery(
    "worker",
    broker=settings.redis_url,
)

celery_app.conf.timezone = "UTC"
celery_app.conf.beat_schedule = {
    "fetch-every-minute": {
        "task": "worker.fetch_prices_task",
        "schedule": 15.0,
    }
}


@celery_app.task(name="worker.fetch_prices_task")
def fetch_prices_task():
    async_to_sync(_fetch_prices)()


async def _fetch_prices():
    client = DeribitClient()
    service = PriceServiceFactory.create()
    await asyncio.gather(_fetch_and_save(client, service, settings.tickers))


async def _fetch_and_save(client: DeribitClient, service, tickers: list[str]):
    prices = []
    try:
        for ticker in tickers:
            price = await client.get_index_price(ticker)
            ts = int(time.time())
            prices.append(Price(ticker=ticker, price=price, ts=ts))
        await service.save_price(prices)
    except Exception as e:
        print(f"Error fetching: {e}")
