import pytest
from app.market.controllers import BASE_CRYPTONATOR_URL


async def test_get_market_price_no_mock(test_cli):
    resp = await test_cli.get('/api/v1/market/get_market_price')
    assert resp.status == 406


async def test_get_market_price_ok(test_cli, mock_responses):
    price = 7714.41340382
    mock_responses.get(f'{BASE_CRYPTONATOR_URL}btc-usd', payload={
        "ticker": {
            "price": str(price),
        }
    })

    resp = await test_cli.get('/api/v1/market/get_market_price')
    assert resp.status == 200
    result = await resp.json()
    assert result['result'] == price


@pytest.mark.parametrize('status,body', [
    (500, b'{}'),
    (200, b'{}'),
    (200, b'[]'),
    (200, b'not a json'),
])
async def test_market_price_bad_response(test_cli, mock_responses, status, body):
    mock_responses.get(f'{BASE_CRYPTONATOR_URL}btc-usd', status=status, body=body)

    resp = await test_cli.get('/api/v1/market/get_market_price')

    assert resp.status == 406
