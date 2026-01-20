import pytest
from app.services.prices_service import PriceService
from app.db.models import Price


@pytest.mark.asyncio
async def test_save_price_calls_repo(mocker):
    mock_save = mocker.patch(
        "app.services.prices_service.PriceRepository.save_price",
        new_callable=mocker.AsyncMock
    )

    service = PriceService()
    prices = [Price(ticker="BTC", price=50000, ts=1670000000)]

    await service.save_price(prices)

    mock_save.assert_awaited_once_with(prices)


@pytest.mark.asyncio
async def test_get_all_prices_returns_repo_result(mocker):
    expected = [Price(ticker="BTC", price=50000, ts=1670000000)]
    mocker.patch(
        "app.services.prices_service.PriceRepository.get_all",
        new_callable=mocker.AsyncMock,
        return_value=expected
    )

    service = PriceService()
    result = await service.get_all_prices("BTC")

    assert result == expected


@pytest.mark.asyncio
async def test_get_last_price_returns_repo_result(mocker):
    expected = Price(ticker="BTC", price=50000, ts=1670000000)
    mocker.patch(
        "app.services.prices_service.PriceRepository.get_last",
        new_callable=mocker.AsyncMock,
        return_value=expected
    )

    service = PriceService()
    result = await service.get_last_price("BTC")

    assert result == expected


@pytest.mark.asyncio
async def test_get_prices_by_date_returns_repo_result(mocker):
    expected = [
        Price(ticker="BTC", price=50000, ts=1670000000),
        Price(ticker="BTC", price=51000, ts=1670003600)
    ]
    mocker.patch(
        "app.services.prices_service.PriceRepository.get_by_date",
        new_callable=mocker.AsyncMock,
        return_value=expected
    )

    service = PriceService()
    ts = 1670000000
    result = await service.get_prices_by_date("BTC", ts)

    assert result == expected
