import asyncio
import logging
from subprocess import PIPE, Popen

import pytest
from aioresponses import aioresponses
from asyncpg import connect

from app.settings import Config
from app.web import create_application

logger = logging.getLogger('conftest')

pytest_plugins = 'aiohttp.pytest_plugin'


@pytest.fixture
def test_cli(loop, aiohttp_client):
    """
    Базовая фикстура для старта приложения и получения aiohttp-клиента
    """
    return loop.run_until_complete(aiohttp_client(create_application()))


async def apply_migrations():
    """
    Запуск процесса миграций ОС асинхронно
    """
    logging.warning('Applying migrations')
    command = f"yoyo apply --database '{Config.DATABASE_URL}' '/migrations' -b"

    proc = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)

    for i in range(10):
        ret_code = proc.poll()
        if ret_code is None:
            await asyncio.sleep(1)
        elif ret_code > 0:
            raise Exception(f'Error during applying migrations: {proc.communicate()}!')
        else:
            return

    raise Exception('Error during applying migrations: timeout!')


@pytest.fixture()
async def db():
    """
    Фикстура для очистки данных в БД и накатки миграций между запусками тестов
    """
    conn = await connect(Config.DATABASE_URL)

    await conn.execute("""
        DROP SCHEMA public CASCADE;
        CREATE SCHEMA public;
    """)

    await apply_migrations()

    await conn.close()


@pytest.fixture(autouse=True)
def mock_responses():
    """
    По умолчанию мокаем все запросы, кроме запросов к серверу
    """
    with aioresponses(passthrough=['http://127.0.0.1:']) as m:
        yield m
