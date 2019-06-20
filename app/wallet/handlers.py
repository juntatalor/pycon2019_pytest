from aiohttp import web

from app.common import ApiError, validate_data
from app.wallet.models import Wallet, WalletOperationError
from app.wallet import schemas

routes_wallet = web.RouteTableDef()


async def _get_wallet_or_404(request: web.Request) -> Wallet:
    """
    Хелпер для получения кошелька по id или ошибки
    """

    try:
        return await Wallet.get(
            request.app['pool'],
            int(request.match_info['wallet_id'])
        )
    except WalletOperationError as e:
        raise ApiError(404, e.message)


@routes_wallet.post('/api/v1/wallets/')
async def create_wallet_handler(request: web.Request):
    """
    Создать кошелек
    """

    wallet = await Wallet.create(request.app['pool'])

    return web.json_response({
        'result': wallet.serialize(),
        'success': True,
        'error': None
    }, status=201)


@routes_wallet.get(r'/api/v1/wallets/{wallet_id:\d+}')
async def get_wallet_handler(request: web.Request):
    wallet = await _get_wallet_or_404(request)

    return web.json_response({
        'result': wallet.serialize(),
        'success': True,
        'error': None
    })


@routes_wallet.post(r'/api/v1/wallets/{wallet_id:\d+}/deposit')
async def deposit_wallet_handler(request: web.Request):

    try:
        data: dict = await request.json()
    except ValueError:
        raise ApiError(400, 'Bad json data')

    validate_data(
        data,
        schemas.SCHEMA_DEPOSIT_HANDLER_BODY
    )

    wallet = await _get_wallet_or_404(request)

    try:
        await wallet.deposit(
            request.app['pool'],
            int(data['value'])
        )
    except WalletOperationError as e:
        raise ApiError(400, e.message)

    return web.json_response({
        'result': wallet.serialize(),
        'success': True,
        'error': None
    })
