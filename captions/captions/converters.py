from collections.abc import Iterable, Iterator

from captions.segment import Segment


def convert_seconds_to_hhmmssmmm(seconds: float, millisecond_separator: str) -> str:
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((seconds % 1) * 1000)

    return f'{int(hours):02}:{int(minutes):02}:{int(seconds):02}{millisecond_separator}{milliseconds:03}'


def segments_to_srt(segments: Iterable[Segment]) -> Iterator[str]:
    return (
        f'{segment.id}\n'
        f'{convert_seconds_to_hhmmssmmm(segment.start, ",")} --> '
        f'{convert_seconds_to_hhmmssmmm(segment.end, ",")}\n{segment.text}'
        for segment in segments
    )


def segments_to_vtt(segments: Iterable[Segment]) -> Iterator[str]:
    yield 'WEBVTT'
    yield from (
        f'{convert_seconds_to_hhmmssmmm(segment.start, ".")} --> '
        f'{convert_seconds_to_hhmmssmmm(segment.end, ".")}\n{segment.text}'
        for segment in segments
    )
