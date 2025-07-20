from typing import BinaryIO, Literal, TypedDict

type CaptionFormat = Literal['srt', 'vtt']

class Arguments(TypedDict):
    file: str | BinaryIO
    caption: CaptionFormat | None
    output: str | None
    cuda: bool
    threads: int | None
    workers: int | None

def parse_args() -> Arguments | None: ...
