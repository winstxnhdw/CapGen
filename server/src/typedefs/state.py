from litestar.datastructures import State

from src.config import Config
from transcriber import Transcriber


class AppState(State):
    config: Config
    transcriber: Transcriber
