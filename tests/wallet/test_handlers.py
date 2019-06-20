from app.wallet.models import Wallet
import pytest


async def test_create_wallet(test_cli):
    resp = await test_cli.post('/api/v1/wallets/')
    assert resp.status == 201
    result = await resp.json()
    assert result['result']['wallet_id']
    assert result['result']['balance'] == 0


async def test_get_wallet(test_cli, new_wallet: Wallet):
    resp = await test_cli.get(f'/api/v1/wallets/{new_wallet.wallet_id}')
    assert resp.status == 200
    result = await resp.json()
    assert result['result']['wallet_id'] == new_wallet.wallet_id


async def test_get_wallet_not_found(test_cli, new_wallet: Wallet):
    resp = await test_cli.get(f'/api/v1/wallets/{new_wallet.wallet_id + 1}')
    assert resp.status == 404
    result = await resp.json()
    assert result['error'] == 'Wallet not found'


@pytest.mark.parametrize('payload', [
    b'',
    b'bad json',
    b'null',
    b'{}',
    b'{"value": "2"}',
])
async def test_deposit_bad_response(test_cli, new_wallet: Wallet, payload):
    resp = await test_cli.post(f'/api/v1/wallets/{new_wallet.wallet_id}/deposit', data=payload)
    assert resp.status == 400
    result = await resp.json()
    assert result['error']


async def test_deposit_not_enough_money(test_cli, new_wallet: Wallet):
    payload = {
        'value': -1
    }
    resp = await test_cli.post(f'/api/v1/wallets/{new_wallet.wallet_id}/deposit', json=payload)
    assert resp.status == 400
    result = await resp.json()
    assert result['error'] == 'Not enough money'


async def test_deposit_ok(test_cli, new_wallet: Wallet):
    payload = {
        'value': 100
    }
    resp = await test_cli.post(f'/api/v1/wallets/{new_wallet.wallet_id}/deposit', json=payload)
    assert resp.status == 200

    payload = {
        'value': -90
    }
    resp = await test_cli.post(f'/api/v1/wallets/{new_wallet.wallet_id}/deposit', json=payload)
    assert resp.status == 200

    result = await resp.json()
    assert result['result']['balance'] == 10
