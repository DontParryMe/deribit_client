from ..services.prices_service import PriceService


class PriceServiceFactory:
    @staticmethod
    def create() -> PriceService:
        return PriceService()
