from __future__ import annotations

from argparse import ArgumentParser
from sys import stdin
from typing import Any


def parse_args() -> dict[str, Any] | None:
    parser = ArgumentParser(description="transcribe a compatible audio/video file into a chosen caption file format")
    parser.add_argument("file", nargs="?", type=str, help="the file path to a compatible audio/video")
    parser.add_argument("-g", "--cuda", action="store_true", help="whether to use CUDA for inference")
    parser.add_argument("-o", "--output", type=str, metavar="", help="the output file path")
    parser.add_argument(
        "-c",
        "--caption",
        type=str,
        metavar="",
        help="the chosen caption file format",
    )

    cpu_group = parser.add_argument_group("cpu")
    cpu_group.add_argument("-t", "--threads", metavar="", type=int, help="the number of CPU threads")
    cpu_group.add_argument("-w", "--workers", metavar="", type=int, help="the number of CPU workers")

    args, unknown = parser.parse_known_args()

    if unknown or (not args.file and stdin.isatty()):
        return parser.print_help()

    return {
        "file": args.file or stdin.buffer,
        "caption": args.caption,
        "output": args.output,
        "cuda": args.cuda,
        "threads": args.threads,
        "workers": args.workers,
    }
