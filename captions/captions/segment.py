from typing import Protocol


class Segment(Protocol):
    id: int
    start: float
    end: float
    text: str
