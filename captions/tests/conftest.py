from typing import NamedTuple

from pytest import fixture


class Segment(NamedTuple):
    id: int
    start: float
    end: float
    text: str


@fixture
def segments() -> tuple[Segment, ...]:
    return (
        Segment(id=1, start=0.0, end=1.72, text="Hello there, my name is Bella."),
        Segment(id=2, start=2.0, end=4.5, text="Welcome to the captions library."),
    )
