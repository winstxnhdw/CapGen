from contextlib import asynccontextmanager
from typing import AsyncIterator

from server.features import Transcriber


@asynccontextmanager
async def load_model(_) -> AsyncIterator[None]:
    """
    Summary
    -------
    download and load the model
    """
    Transcriber.load()
    yield
