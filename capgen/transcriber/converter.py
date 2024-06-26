from typing import Iterable

from faster_whisper.transcribe import Segment

from capgen.utils import convert_seconds_to_hhmmssmmm


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
        subrip_subtitle (str) : the SRT subtitles
        """
        return '\n\n'.join(
            f'{segment.id}\n'
            f'{convert_seconds_to_hhmmssmmm(segment.start, ",")} --> '
            f'{convert_seconds_to_hhmmssmmm(segment.end, ",")}\n{segment.text[1:]}'
            for segment in segments
        )

    def to_vtt(self, segments: Iterable[Segment]) -> str:
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
        captions = '\n\n'.join(
            f'{convert_seconds_to_hhmmssmmm(segment.start, ".")} --> '
            f'{convert_seconds_to_hhmmssmmm(segment.end, ".")}\n{segment.text[1:]}'
            for segment in segments
        )

        return f'WEBVTT\n\n{captions}'
