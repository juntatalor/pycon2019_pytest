import asyncio
import logging

from aiohttp.web import Application, run_app
from asyncpg import create_pool
from app.system.handlers import routes_system
from app.market.handlers import routes_market
from app.wallet.handlers import routes_wallet
from app.common import error_middleware

from app.settings import Config

logger = logging.getLogger('app')

logging.basicConfig(level=logging.INFO)


async def _setup(app: Application):
    app['pool'] = await create_pool(Config.DATABASE_URL)
    logger.info('Database connection pool created')


async def _teardown(app: Application):
    await app['pool'].close()
    logger.info('Database connection pool closed')


def create_application():
    application = Application(
        middlewares=[error_middleware],
        debug=Config.DEBUG
    )

    application.on_startup.append(_setup)
    application.on_cleanup.append(_teardown)

    application.router.add_routes(routes_system)
    application.router.add_routes(routes_market)
    application.router.add_routes(routes_wallet)

    return application


def run():
    run_app(
        create_application(),
        host='0.0.0.0',
        port=Config.PORT
    )
