import pytest

from app.wallet.models import Wallet


@pytest.fixture
async def new_wallet(test_cli) -> Wallet:

    pool = test_cli.app['pool']

    wallet = await Wallet.create(pool)

    yield wallet

    await wallet.delete(pool)
