from aiohttp import web

from app.system.controllers import check_db

routes_system = web.RouteTableDef()


@routes_system.get('/healthcheck')
async def health_check_handler(request: web.Request):
    """
    Проверка состояния приложения
    """
    await check_db(request.app['pool'])

    return web.json_response({
        'result': True,
        'success': True,
        'error': None
    })

