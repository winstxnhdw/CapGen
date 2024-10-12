from typing import BinaryIO, Iterator, Literal

from av.error import InvalidDataError
from faster_whisper import WhisperModel

from capgen.transcriber.caption_format import CaptionFormat
from capgen.transcriber.converter import Converter


class Transcriber:
    """
    Summary
    -------
    a wrapper class for faster-whisper

    Methods
    -------
    transcribe(file: str | BinaryIO, caption_format: str) -> str | None:
        converts transcription segments into a specific caption format
    """

    __slots__ = ('model',)

    def __init__(self, device: Literal['auto', 'cpu', 'cuda'], number_of_threads: int = 0, number_of_workers: int = 1):
        self.model = WhisperModel(
            'Systran/faster-distil-whisper-large-v3',
            device,
            compute_type='auto',
            cpu_threads=number_of_threads,
            num_workers=number_of_workers,
        )

    def transcribe(self, file: str | BinaryIO, caption_format: CaptionFormat) -> Iterator[str] | None:
        """
        Summary
        -------
        transcribes a compatible audio/video into a chosen caption format

        Parameters
        ----------
        file (str | BinaryIO) : the file to transcribe
        caption_format (str) : the chosen caption format

        Returns
        -------
        transcription (Iterator[str] | None) : the transcribed text in the chosen caption format
        """
        try:
            segments, _ = self.model.transcribe(
                file,
                language='en',
                beam_size=1,
                vad_filter=True,
                vad_parameters={'min_silence_duration_ms': 500},
            )

        except InvalidDataError:
            return None

        converter = Converter(segments)

        if caption_format == 'srt':
            return converter.to_srt()

        if caption_format == 'vtt':
            return converter.to_vtt()

        return (segment.text for segment in segments)
