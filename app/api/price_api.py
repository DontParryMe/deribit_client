from fastapi import APIRouter, HTTPException, Query

from ..factories.price_factory import PriceServiceFactory


class PriceAPI:
    def __init__(self):
        self.router = APIRouter(prefix="/prices", tags=["Prices"])

        self.router.add_api_route("/all", self.get_all, methods=["GET"])
        self.router.add_api_route("/last", self.get_last, methods=["GET"])
        self.router.add_api_route("/by-date", self.get_by_date, methods=["GET"])

    async def get_all(self, ticker: str = Query(...)):
        service = PriceServiceFactory.create()
        result = await service.get_all_prices(ticker)
        return [{"ticker": p.ticker, "price": float(p.price), "ts": p.ts} for p in result]

    async def get_last(self, ticker: str = Query(...)):
        service = PriceServiceFactory.create()
        price = await service.get_last_price(ticker)
        if not price:
            raise HTTPException(status_code=404, detail="No data")
        return {"ticker": price.ticker, "price": float(price.price), "ts": price.ts}

    async def get_by_date(self, ticker: str = Query(...), ts: int = Query(..., description="UNIX timestamp")):
        service = PriceServiceFactory.create()
        result = await service.get_prices_by_date(ticker, ts)
        return [{"ticker": p.ticker, "price": float(p.price), "ts": p.ts} for p in result]
