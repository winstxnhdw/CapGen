from typing import BinaryIO, NamedTuple

from capgen.transcriber import CaptionFormat


class Arguments(NamedTuple):
    """
    Summary
    -------
    the arguments for the command line interface

    Attributes
    ----------
    file (str | BinaryIO) : the file path to a compatible audio/video
    caption (Literal['srt', 'vtt']) : the chosen caption file format
    output (str) : the output file path
    cuda (bool) : whether to use CUDA for inference
    """

    file: str | BinaryIO
    caption: CaptionFormat
    output: str
    cuda: bool
    threads: int | None
    workers: int | None
