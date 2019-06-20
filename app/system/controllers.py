import asyncio
from app.common import ApiError
from asyncpg import PostgresError
from asyncpg.pool import Pool


async def check_db(pool: Pool):
    """
    Проверяет работоспособность БД
    """

    try:
        async with pool.acquire(timeout=1) as conn:
            await conn.execute('select 1', timeout=1)
    except asyncio.TimeoutError:
        raise ApiError(500, 'Database timeout error')
    except PostgresError as e:
        raise ApiError(500, 'Database error: %s' % str(e))
