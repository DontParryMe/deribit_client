from datetime import datetime, timezone

from sqlalchemy import select

from ..db.database import Database
from ..db.models import Price


class PriceRepository:
    def __init__(self):
        self._db = Database()

    async def save_price(self, prices: list[Price]):
        async with self._db.get_session() as session:
            for price in prices:
                session.add(price)
            await session.commit()

    async def get_all(self, ticker: str):
        async with self._db.get_session() as session:
            stmt = select(Price).where(Price.ticker == ticker).order_by(Price.ts)
            result = await session.execute(stmt)
            return result.scalars().all()

    async def get_last(self, ticker: str):
        async with self._db.get_session() as session:
            stmt = select(Price).where(Price.ticker == ticker).order_by(Price.ts.desc()).limit(1)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def get_by_date(self, ticker: str, ts: int):
        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
        day_start = int(datetime(dt.year, dt.month, dt.day, tzinfo=timezone.utc).timestamp())
        day_end = int(datetime(dt.year, dt.month, dt.day, 23, 59, 59, 999999, tzinfo=timezone.utc).timestamp())

        async with self._db.get_session() as session:
            stmt = select(Price).where(Price.ticker == ticker, Price.ts.between(day_start, day_end)).order_by(Price.ts)
            result = await session.execute(stmt)
            return result.scalars().all()
