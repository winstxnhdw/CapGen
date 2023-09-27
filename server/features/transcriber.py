from typing import BinaryIO, Literal

from capgen.transcriber import Transcriber as WhisperTranscriber


class Transcriber:
    """
    Summary
    -------
    a static class for transcribing audio/video files into a chosen caption format

    Methods
    -------
    transcribe(file: str | BinaryIO, transcription_type: Literal['srt']) -> str:
        converts transcription segments into a SRT file
    """
    transcriber = WhisperTranscriber('cpu', number_of_workers=2)

    @classmethod
    def transcribe(cls, file: str | BinaryIO, transcription_type: Literal['srt']) -> str | None:
        """
        Summary
        -------
        transcribes a compatible audio/video into a chosen caption format

        Parameters
        ----------
        file (str | BinaryIO) : the file to transcribe
        transcription_type (Literal['srt']) : the chosen caption format

        Returns
        -------
        transcription (str | None) : the transcribed text in the chosen caption format
        """
        return cls.transcriber.transcribe(file, transcription_type)