from collections.abc import Iterable, Iterator
from typing import Protocol

class Segment(Protocol):
    id: int
    start: float
    end: float
    text: str

def segments_to_srt(segments: Iterable[Segment]) -> Iterator[str]: ...
def segments_to_vtt(segments: Iterable[Segment]) -> Iterator[str]: ...
