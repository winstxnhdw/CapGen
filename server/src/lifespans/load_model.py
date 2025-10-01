from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from src.lifespans.inject_state import inject_state
from src.typedefs import AppState
from transcriber import Transcriber


@inject_state
@asynccontextmanager
async def load_model(_, state: AppState) -> AsyncIterator[None]:
    with Transcriber("cpu", number_of_workers=state.config.worker_count) as transcriber:
        state.transcriber = transcriber
        yield
