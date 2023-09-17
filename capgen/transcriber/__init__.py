from typing import BinaryIO, Literal, TypedDict

from faster_whisper import WhisperModel

from capgen.transcriber.converter import Converter
from capgen.types import TranscriberOptions


class Transcriber:
    """
    Summary
    -------
    a static class for faster-whisper transcriber

    Methods
    -------
    transcribe(file: str | BinaryIO, caption_format: Literal['srt']) -> str:
        converts transcription segments into a SRT file
    """
    base_options = TranscriberOptions(
        model_size_or_path='guillaumekln/faster-whisper-large-v2',
        compute_type='auto',
        num_workers=4,
    )

    model = WhisperModel(**base_options, device='cpu')

    @classmethod
    def toggle_device(cls):
        """
        Summary
        -------
        toggles the device between CPU and GPU
        """
        cls.model = WhisperModel(
            **cls.base_options,
            device='cpu' if cls.model.model.device == 'cuda' else 'cuda',
        )


    @classmethod
    def transcribe(cls, file: str | BinaryIO, caption_format: Literal['srt']) -> str:
        """
        Summary
        -------
        transcribes a compatible audio/video into a chosen caption format

        Parameters
        ----------
        file (str | BinaryIO) : the file to transcribe
        caption_format (Literal['srt']) : the chosen caption format

        Returns
        -------
        transcription (str) : the transcribed text in the chosen caption format
        """
        segments, _ = cls.model.transcribe(
            file,
            vad_filter=True,
            vad_parameters={ 'min_silence_duration_ms': 500 }
        )

        converter = Converter(segments)

        if caption_format == 'srt':
            return converter.to_srt(segments)

        raise KeyError(f'Invalid format: {caption_format}!')
