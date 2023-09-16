from argparse import ArgumentParser
from typing import Literal, NamedTuple

from server.features import Transcriber


class Arguments(NamedTuple):
    """
    Summary
    -------
    """
    file: str
    type: Literal['srt']
    output: str
    cuda: bool


def parse_args() -> tuple[Arguments, list[str]]:
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
    parser.add_argument('-c', '--cuda',   action='store_true', help='whether to use CUDA for inference')

    required_group = parser.add_argument_group('required')
    required_group.add_argument('-f', '--file',   type=str, required=True, metavar='', help='the file path to a compatible audio/video')
    required_group.add_argument('-t', '--type',   type=str, required=True, metavar='', help='the chosen caption file format')
    required_group.add_argument('-o', '--output', type=str, required=True, metavar='', help='the output file path')

    return parser.parse_known_args()  # type: ignore


def main():
    """
    Summary
    -------
    """
    args, _ = parse_args()

    if args.cuda:
        Transcriber.toggle_device()

    transcription = Transcriber.transcribe(args.file, args.type)

    with open(args.output, 'w', encoding='utf-8') as file:
        file.write(transcription)


if __name__ == '__main__':
    main()
