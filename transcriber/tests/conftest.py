from collections.abc import Iterator
from pathlib import Path
from typing import BinaryIO, Literal

from pytest import fixture

from transcriber import Transcriber


@fixture(scope="session")
def anyio_backend() -> tuple[Literal["asyncio", "trio"], dict[str, bool]]:
    return "asyncio", {"use_uvloop": True}


@fixture(scope="session")
def transcriber() -> Iterator[Transcriber]:
    with Transcriber("cpu") as transcriber:
        yield transcriber


@fixture
def audio_file_path() -> Path:
    return Path("tests/test.mp3")


@fixture
def audio_file(audio_file_path: Path) -> Iterator[BinaryIO]:
    with audio_file_path.open("rb") as file:
        yield file
