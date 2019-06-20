from aiohttp import web

from app.market.controllers import get_market_price

routes_market = web.RouteTableDef()


@routes_market.get('/api/v1/market/get_market_price')
async def get_market_price_handler(request: web.Request):
    """
    Получает цену фиатной валюты из внешнего сервиса
    """
    price = await get_market_price()

    return web.json_response({
        'result': price,
        'success': True,
        'error': None
    })
