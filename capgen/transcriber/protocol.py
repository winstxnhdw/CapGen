from typing import BinaryIO, Protocol


class TranscriberProtocol(Protocol):
    """
    Summary
    -------
    a protocol for all transcriber(s)

    Methods
    -------
    transcribe(file: str | BinaryIO, caption_format: str) -> str | None:
        converts transcription segments into a specific caption format
    """

    __slots__ = ('model',)

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
