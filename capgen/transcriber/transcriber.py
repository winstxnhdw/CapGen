from typing import BinaryIO, Literal

from faster_whisper import WhisperModel

from capgen.transcriber.converter import Converter


class Transcriber:
    """
    Summary
    -------
    a wrapper class for faster-whisper

    Methods
    -------
    transcribe(file: str | BinaryIO, caption_format: Literal['srt']) -> str | None:
        converts transcription segments into a SRT file
    """
    __slots__ = ('model',)

    def __init__(
        self,
        device: Literal['auto', 'cpu', 'cuda'],
        number_of_threads: int = 0,
        number_of_workers: int = 1
    ):

        self.model = WhisperModel(
            'distil-whisper/distil-large-v3-ct2',
            device,
            compute_type='auto',
            cpu_threads=number_of_threads,
            num_workers=number_of_workers
        )


    def transcribe(self, file: str | BinaryIO, caption_format: str) -> str | None:
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
        transcription (str | None) : the transcribed text in the chosen caption format
        """
        segments, _ = self.model.transcribe(
            file,
            vad_filter=True,
            vad_parameters={ 'min_silence_duration_ms': 500 }
        )

        converter = Converter(segments)

        if caption_format == 'srt':
            return converter.to_srt(segments)

        if caption_format == 'vtt':
            raise NotImplementedError('VTT format is not yet supported!')

        return None
