from collections.abc import AsyncIterator, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from logging import Logger

from litestar import Litestar

from transcriber import Transcriber


@asynccontextmanager
async def transcriber_lifespan(
    app: Litestar,
    *,
    logger: Logger,
    use_cuda: bool,
    worker_count: int,
) -> AsyncIterator[None]:
    with Transcriber("cuda" if use_cuda else "cpu", number_of_workers=worker_count, logger=logger) as transcriber:
        app.state.transcriber = transcriber
        yield


def load_transcriber_model(
    *,
    logger: Logger,
    use_cuda: bool,
    worker_count: int,
) -> Callable[[Litestar], AbstractAsyncContextManager[None]]:
    return lambda app: transcriber_lifespan(app, logger=logger, use_cuda=use_cuda, worker_count=worker_count)
