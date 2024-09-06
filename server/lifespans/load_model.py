from contextlib import asynccontextmanager
from typing import AsyncIterator

from litestar import Litestar

from capgen.transcriber import Transcriber
from server.config import Config


@asynccontextmanager
async def load_model(app: Litestar) -> AsyncIterator[None]:
    """
    Summary
    -------
    download and load the model
    """
    app.state.transcriber = Transcriber('cpu', number_of_workers=Config.worker_count)

    try:
        yield
    finally:
        pass
