from typing import BinaryIO, Iterable, Literal

from faster_whisper import WhisperModel
from faster_whisper.transcribe import Segment


class Transcriber:
    """
    Summary
    -------
    a static class for faster-whisper transcriber

    Methods
    -------
    transcribe(file: str | BinaryIO, transcription_type: Literal['srt']) -> str:
        converts transcription segments into a SRT file
    """
    model = WhisperModel('large-v2', device="cpu", compute_type='auto')

    @classmethod
    def toggle_device(cls):
        """
        Summary
        -------
        toggles the device between CPU and GPU
        """
        cls.model = WhisperModel(
            'large-v2',
            device="cpu" if cls.model.model.device == "cuda" else "cuda",
            compute_type='auto'
        )


    @classmethod
    def convert_seconds_to_hhmmssmmm(cls, seconds: float) -> str:
        """
        Summary
        -------
        converts seconds to hh:mm:ss,mmm format

        Parameters
        ----------
        seconds (float) : the number of seconds to convert

        Returns
        -------
        converted_time (str) : the converted time in hh:mm:ss,mmm format
        """
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = int((seconds % 1) * 1000)

        return f'{int(hours):02}:{int(minutes):02}:{int(seconds):02},{milliseconds:03}'


    @classmethod
    def as_srt(cls, segments: Iterable[Segment]) -> str:
        """
        Summary
        -------
        converts transcription segments into a SRT file

        Parameters
        ----------
        segments (Iterable[Segment]) : the segments to convert

        Returns
        -------
        subrip_subtitle (str) : the SRT file
        """
        return '\n\n'.join(
            f'{segment.id}\n'
            f'{cls.convert_seconds_to_hhmmssmmm(segment.start)} --> '
            f'{cls.convert_seconds_to_hhmmssmmm(segment.end)}\n{segment.text.strip()}'
            for segment in segments
        )


    @classmethod
    def transcribe(cls, file: str | BinaryIO, transcription_type: Literal['srt']) -> str:
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
        transcription (str) : the transcribed text in the chosen caption format
        """
        segments, _ = cls.model.transcribe(file, vad_filter=True)

        if transcription_type == 'srt':
            return cls.as_srt(segments)

        raise KeyError(f'Invalid transcription type: {transcription_type}!')
