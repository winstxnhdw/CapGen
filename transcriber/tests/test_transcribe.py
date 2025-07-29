# ruff: noqa: S101, PLR2004

from __future__ import annotations

from pathlib import Path
from typing import BinaryIO

from pytest import mark, raises

from transcriber import Transcriber


def test_transcribe_from_file(transcriber: Transcriber, audio_file: BinaryIO) -> None:
    assert next(transcriber.transcribe(audio_file)).text == 'Hello there, my name is Bella.'


def test_transcribe_from_path(transcriber: Transcriber, audio_file_path: Path) -> None:
    assert next(transcriber.transcribe(audio_file_path)).text == 'Hello there, my name is Bella.'


def test_transcribe_invalid_file(transcriber: Transcriber) -> None:
    with raises(StopIteration):
        next(transcriber.transcribe('invalid_file.mp3'))


def test_transcribe_invalid_data(transcriber: Transcriber) -> None:
    with raises(StopIteration), Path('pyproject.toml').open('rb') as file:
        next(transcriber.transcribe(file))


@mark.flaky
def test_transcribe_timings(transcriber: Transcriber, audio_file: BinaryIO) -> None:
    transcription = next(transcriber.transcribe(audio_file))
    assert transcription.start == 0.0
    assert transcription.end == 1.72
