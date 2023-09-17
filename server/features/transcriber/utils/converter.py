from typing import Iterable

from faster_whisper.transcribe import Segment


class Converter:
    """
    Summary
    -------
    a class for converting transcriptions into various caption formats

    Attributes
    ----------
    segments (Iterable[Segment]) : the segments to convert

    Methods
    -------
    convert_seconds_to_hhmmssmmm(seconds: float) -> str:
        converts seconds to hh:mm:ss,mmm format

    as_srt(segments: Iterable[Segment]) -> str:
        converts transcription segments into a SRT file
    """
    def __init__(self, segments: Iterable[Segment]):
        self.segments = segments


    def convert_seconds_to_hhmmssmmm(self, seconds: float) -> str:
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


    def to_srt(self, segments: Iterable[Segment]) -> str:
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
            f'{self.convert_seconds_to_hhmmssmmm(segment.start)} --> '
            f'{self.convert_seconds_to_hhmmssmmm(segment.end)}\n{segment.text.strip()}'
            for segment in segments
        )
