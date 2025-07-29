from __future__ import annotations

from collections.abc import Iterator
from logging import Logger, getLogger
from typing import BinaryIO, Literal, Self

from av.error import FileNotFoundError as AVFileNotFoundError
from av.error import InvalidDataError
from faster_whisper import WhisperModel
from faster_whisper.transcribe import Segment


class Transcriber:
    __slots__ = ('logger', 'model')

    def __init__(
        self,
        device: Literal['auto', 'cpu', 'cuda'],
        number_of_threads: int = 0,
        number_of_workers: int = 1,
        logger: Logger | None = None,
    ) -> None:
        self.logger = logger or getLogger(__name__)
        self.model = WhisperModel(
            'Systran/faster-distil-whisper-large-v3',
            device,
            compute_type='auto',
            cpu_threads=number_of_threads,
            num_workers=number_of_workers,
        )

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_) -> None:
        del self.model

    def transcribe(self, file: str | BinaryIO) -> Iterator[Segment]:
        try:
            segments, _ = self.model.transcribe(
                file,
                language='en',
                beam_size=1,
                vad_filter=True,
                vad_parameters={'min_silence_duration_ms': 500},
            )

        except (InvalidDataError, IndexError):
            self.logger.exception('Invalid audio file provided: %s', file)
            return

        except AVFileNotFoundError:
            self.logger.exception('Audio file not found: %s', file)
            return

        segment: Segment = next(segments)  # pyright: ignore [reportArgumentType]
        segment.text = segment.text.lstrip()
        yield segment
        yield from segments
