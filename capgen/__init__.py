from argparse import ArgumentParser
from typing import Literal, NamedTuple

from capgen.transcriber import Transcriber


class Arguments(NamedTuple):
    """
    Summary
    -------
    the arguments for the command line interface

    Attributes
    ----------
    file (str) : the file path to a compatible audio/video
    caption (Literal['srt']) : the chosen caption file format
    output (str) : the output file path
    cuda (bool) : whether to use CUDA for inference
    """
    file: str
    caption: Literal['srt']
    output: str
    cuda: bool


def parse_args() -> Arguments:
    """
    Summary
    -------
    parses the command line arguments

    Returns
    -------
    args (Arguments) : the parsed arguments
    unknown (list[str]) : the unknown arguments
    """
    parser = ArgumentParser(description='Transcribe a compatible audio/video file into a chosen caption file')
    parser.add_argument('-g', '--cuda',   action='store_true', help='whether to use CUDA for inference')

    required_group = parser.add_argument_group('required')
    required_group.add_argument('-f', '--file',    type=str, required=True, metavar='', help='the file path to a compatible audio/video')
    required_group.add_argument('-c', '--caption', type=str, required=True, metavar='', help='the chosen caption file format')
    required_group.add_argument('-o', '--output',  type=str, required=True, metavar='', help='the output file path')

    return parser.parse_known_args()[0]  # type: ignore


def main():
    """
    Summary
    -------
    the entrypoint for the CapGen CLI
    """
    args = parse_args()

    if args.cuda:
        Transcriber.toggle_device()

    transcription = Transcriber.transcribe(args.file, args.caption)

    with open(args.output, 'w', encoding='utf-8') as file:
        file.write(transcription)


if __name__ == '__main__':
    main()
