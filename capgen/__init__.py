from argparse import ArgumentParser
from ctypes import CDLL
from os import name
from os.path import join
from site import getsitepackages
from sys import stdin

from capgen.transcriber import Transcriber
from capgen.types import Arguments, TranscriberOptions


class InvalidFormatError(Exception):
    """
    Summary
    -------
    an exception for invalid caption formats
    """


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

    cpu_group = parser.add_argument_group('cpu')
    cpu_group.add_argument('-t', '--threads', metavar='', type=int, help='the number of CPU threads')
    cpu_group.add_argument('-w', '--workers', metavar='', type=int, help='the number of CPU workers')

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
        args.cuda,
        args.threads,
        args.workers
    )


def resolve_cuda_libraries():
    """
    Summary
    -------
    resolves the CUDA libraries
    """
    site_package_path = join(getsitepackages()[-1], 'nvidia')

    try:
        if name == 'nt':
            CDLL(join(site_package_path, 'cudnn', 'bin', 'cudnn_cnn_infer64_8.dll'))

        else:
            CDLL(join(site_package_path, 'cudnn', 'lib', 'libcudnn_cnn_infer.so.8'))

    except OSError:
        print('Unable to find Python cuDNN binaries, falling back to system binaries..')

    try:
        if name == 'nt':
            CDLL(join(site_package_path, 'cublas', 'bin', 'cublas64_12.dll'))

        else:
            CDLL(join(site_package_path, 'cublas', 'lib', 'libcublas.so.12'))

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

    options = TranscriberOptions(device='cpu')

    if args.threads:
        options['number_of_threads'] = args.threads

    if args.workers:
        options['number_of_workers'] = args.workers

    if args.cuda:
        options['device'] = 'cuda'
        resolve_cuda_libraries()

    if not (transcription := Transcriber(**options).transcribe(args.file, args.caption)):
        raise InvalidFormatError(f'Invalid format: {args.caption}!')

    with open(args.output, 'w', encoding='utf-8') as file:
        file.write(transcription)


if __name__ == '__main__':
    main()
