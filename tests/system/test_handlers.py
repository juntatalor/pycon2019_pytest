from asyncpg.exceptions import PostgresError


async def test_health_check_ok(test_cli):
    resp = await test_cli.get('/healthcheck')
    assert resp.status == 200
    assert await resp.json() == {'result': True, 'error': None, 'success': True}


async def test_health_check_db_err(test_cli, monkeypatch):
    pg_error = 'mock_error'

    async def conn_raise_err(*args, **kwargs):
        raise PostgresError(pg_error)

    monkeypatch.setattr('asyncpg.connection.Connection.execute', conn_raise_err)

    resp = await test_cli.get('/healthcheck')
    assert resp.status == 500
    assert await resp.json() == {'error': 'Database error: %s' % pg_error, 'success': False}
