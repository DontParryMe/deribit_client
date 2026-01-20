from ..db.models import Price
from ..repositories.prices_repository import PriceRepository


class PriceService:
    def __init__(self):
        self._repo = PriceRepository()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def save_price(self, prices: list[Price]):
        """Сохранить цену валюты"""
        await self._repo.save_price(prices)

    async def get_all_prices(self, ticker: str):
        """Получить все цены по валюте"""
        return await self._repo.get_all(ticker)

    async def get_last_price(self, ticker: str):
        """Получить последнюю цену по валюте"""
        return await self._repo.get_last(ticker)

    async def get_prices_by_date(self, ticker: str, ts: int):
        """Получить цены за день, содержащий timestamp"""
        return await self._repo.get_by_date(ticker, ts)
