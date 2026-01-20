import aiohttp

from ..core.config import get_settings

settings = get_settings()


class DeribitClient:
    BASE_URL = settings.deribit_base_url

    async def get_index_price(self, ticker: str) -> float:
        url = f"{self.BASE_URL}/public/get_index_price"
        params = {"index_name": ticker}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                data = await resp.json()
                if "result" not in data:
                    raise ValueError(f"Unexpected response from Deribit: {data}")
                return float(data["result"]["index_price"])
