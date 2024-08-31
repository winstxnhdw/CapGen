# pylint: disable=missing-function-docstring,redefined-outer-name

from typing import AsyncIterator

from litestar import Litestar
from litestar.testing import AsyncTestClient
from pytest import fixture

from server import app


@fixture(scope='function')
async def client() -> AsyncIterator[AsyncTestClient[Litestar]]:
    async with AsyncTestClient(app=app) as client:
        yield client
