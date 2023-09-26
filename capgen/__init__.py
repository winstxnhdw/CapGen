from argparse import ArgumentParser
from ctypes import CDLL
from os.path import join
from site import getsitepackages
from sys import stdin
from typing import BinaryIO, Literal, NamedTuple

from capgen.transcriber import Transcriber


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


def parse_args() -> Arguments | None:
    """
    Summary
    -------
    parses the command line arguments

    Returns
    -------
    args (Arguments) : the parsed arguments
    """
    parser = ArgumentParser(description='transcribe a compatible audio/video file into a chosen caption file format')
    parser.add_argument('file', nargs='?', type=str, help='the file path to a compatible audio/video')
    parser.add_argument('-g', '--cuda',   action='store_true', help='whether to use CUDA for inference')

    required_group = parser.add_argument_group('required')
    required_group.add_argument('-c', '--caption', type=str, required=True, metavar='', help='the chosen caption file format')
    required_group.add_argument('-o', '--output',  type=str, required=True, metavar='', help='the output file path')

    args, unknown = parser.parse_known_args()

    if unknown or not args.file and stdin.isatty():
        return parser.print_help()

    return Arguments(
        args.file or stdin.buffer,
        args.caption,
        args.output,
        args.cuda
    )

def resolve_cuda_libraries():
    """
    Summary
    -------
    resolves the CUDA libraries
    """
    site_package_path = join(getsitepackages()[0], 'nvidia')

    try:
        CDLL(join(site_package_path, 'cudnn', 'lib', 'libcudnn_cnn_infer.so.8'))

    except OSError:
        print('Unable to find Python cuDNN binaries, falling back to system binaries..')

    try:
        CDLL(join(site_package_path, 'cublas', 'lib', 'libcublas.so.11'))

    except OSError:
        print('Unable to find Python cuBLAS binaries, falling back to system binaries..')


def main():
    """
    Summary
    -------
    the entrypoint for the CapGen CLI
    """
    if not (args := parse_args()):
        return

    if args.cuda:
        resolve_cuda_libraries()
        Transcriber.toggle_device()

    transcription = Transcriber.transcribe(args.file, args.caption)

    with open(args.output, 'w', encoding='utf-8') as file:
        file.write(transcription)


if __name__ == '__main__':
    main()
