from typing import BinaryIO, Literal, TypedDict

from faster_whisper import WhisperModel

from capgen.transcriber.converter import Converter


class WhisperParameters(TypedDict):
    """
    Summary
    -------
    a type hint for the parameters of the WhisperModel class
    """

    model_size_or_path: str
    device: str
    compute_type: str
    cpu_threads: int
    num_workers: int


class Transcriber:
    """
    Summary
    -------
    a wrapper class for faster-whisper

    Methods
    -------
    transcribe(file: str | BinaryIO, caption_format: str) -> str | None:
        converts transcription segments into a SRT file
    """

    __slots__ = ('model',)

    def __init__(
        self,
        device: Literal['auto', 'cpu', 'cuda'],
        number_of_threads: int = 0,
        number_of_workers: int = 1,
    ):
        model_parameters: WhisperParameters = {
            'model_size_or_path': 'Systran/faster-distil-whisper-large-v3',
            'device': device,
            'compute_type': 'auto',
            'cpu_threads': number_of_threads,
            'num_workers': number_of_workers,
        }

        try:
            self.model = WhisperModel(**model_parameters, flash_attention=True)

        except Exception:  # pylint: disable=broad-except
            self.model = WhisperModel(**model_parameters)

    async def transcribe(self, file: str | BinaryIO, caption_format: str) -> str | None:
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
            beam_size=1,
            vad_filter=True,
            vad_parameters={'min_silence_duration_ms': 500},
        )

        converter = Converter(segments)

        if caption_format == 'srt':
            return converter.to_srt(segments)

        if caption_format == 'vtt':
            return converter.to_vtt(segments)

        return None
