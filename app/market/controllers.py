import aiohttp
from app.common import ApiError
from urllib.parse import urljoin

BASE_CRYPTONATOR_URL = 'https://api.cryptonator.com/api/full/'


async def _do_get_market_price(resp: aiohttp.ClientResponse):

    if resp.status != 200:
        raise ApiError(
            406,
            message='Bad status from cryptonator: %s'
                    % resp.status
        )

    try:
        result = await resp.json()
    except ValueError:
        raise ApiError(
            406,
            message='Bad response from cryptonator (not a json)'
        )

    try:
        return float(result['ticker']['price'])
    except (TypeError, KeyError, ValueError):
        raise ApiError(
            406,
            message='Bad response from cryptonator (bad format)'
        )


async def get_market_price(ticker: str = 'btc-usd') -> float:
    url = urljoin(BASE_CRYPTONATOR_URL, ticker)
    try:
        async with aiohttp.request('GET', url) as resp:
            return await _do_get_market_price(resp)
    except aiohttp.ClientError as e:
        raise ApiError(
            406,
            message='Bad response from cryptonator (%s)'
                    % e
        )
