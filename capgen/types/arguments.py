from typing import BinaryIO, Literal, NamedTuple


class Arguments(NamedTuple):
    """
    Summary
    -------
    the arguments for the command line interface

    Attributes
    ----------
    file (str | BinaryIO) : the file path to a compatible audio/video
    caption (Literal['srt']) : the chosen caption file format
    output (str) : the output file path
    cuda (bool) : whether to use CUDA for inference
    """
    file: str | BinaryIO
    caption: Literal['srt']
    output: str
    cuda: bool
    threads: int | None
    workers: int | None
