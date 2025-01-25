from typing import Iterable, Iterator

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
    convert_seconds_to_hhmmssmmm(seconds: float, millisecond_separator: str) -> str:
        converts seconds to hh:mm:ss,mmm format

    to_srt() -> str:
        converts transcription segments into a SRT file

    to_vtt() -> str:
        converts transcription segments into a VTT file
    """

    __slots__ = ('segments',)

    def __init__(self, segments: Iterable[Segment]):
        self.segments = segments

    def convert_seconds_to_hhmmssmmm(self, seconds: float, millisecond_separator: str) -> str:
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

        return f'{int(hours):02}:{int(minutes):02}:{int(seconds):02}{millisecond_separator}{milliseconds:03}'

    def to_srt(self) -> Iterator[str]:
        """
        Summary
        -------
        converts transcription segments into a SRT file

        Parameters
        ----------
        segments (Iterable[Segment]) : the segments to convert

        Returns
        -------
        subrip_subtitle (str) : the SRT subtitles
        """
        return (
            f'{id}\n'
            f'{self.convert_seconds_to_hhmmssmmm(segment.start, ",")} --> '
            f'{self.convert_seconds_to_hhmmssmmm(segment.end, ",")}\n{segment.text[1:]}'
            for segment in self.segments
        )

    def to_vtt(self) -> Iterator[str]:
        """
        Summary
        -------
        converts transcription segments into a VTT file

        Parameters
        ----------
        segments (Iterable[Segment]) : the segments to convert

        Returns
        -------
        video_text_tracks_subtitle (str) : the VTT subtitles
        """
        yield 'WEBVTT'
        yield from (
            f'{self.convert_seconds_to_hhmmssmmm(segment.start, ".")} --> '
            f'{self.convert_seconds_to_hhmmssmmm(segment.end, ".")}\n{segment.text[1:]}'
            for segment in self.segments
        )
