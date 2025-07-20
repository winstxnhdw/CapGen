from collections.abc import AsyncIterator
from typing import Literal

from anyio import open_file
from litestar import Litestar
from litestar.testing import AsyncTestClient
from pytest import fixture
from src.app import app


@fixture(scope='session')
def anyio_backend() -> tuple[Literal['asyncio', 'trio'], dict[str, bool]]:
    return 'asyncio', {'use_uvloop': True}


@fixture(scope='session')
async def session_client() -> AsyncIterator[AsyncTestClient[Litestar]]:
    async with AsyncTestClient(app=app()) as client:
        yield client


@fixture(scope='session')
async def audio_file() -> AsyncIterator[bytes]:
    async with await open_file('tests/test.mp3', 'rb') as file:
        yield await file.read()
