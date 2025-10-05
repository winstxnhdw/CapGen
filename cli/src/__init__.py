from __future__ import annotations

from ctypes import CDLL
from logging import getLogger
from os import name
from pathlib import Path
from site import getsitepackages
from sys import stdout
from typing import BinaryIO

from captions import segments_to_srt, segments_to_vtt
from src.parse_args import parse_args
from src.typedefs import TranscriberOptions
from transcriber import Transcriber


class InvalidFileFormatError(Exception):
    def __init__(self, file: str | BinaryIO) -> None:
        super().__init__(f"Invalid format for file: {file}")


def resolve_cuda_libraries() -> None:
    logger = getLogger(__name__)
    site_package_path = Path(getsitepackages()[-1]) / "nvidia"
    cudnn_path = site_package_path / "cudnn"
    cublas_path = site_package_path / "cublas"

    try:
        if name == "nt":
            CDLL(cudnn_path / "bin" / "cudnn_cnn_infer64_8.dll")

        else:
            CDLL(cudnn_path / "lib" / "libcudnn_cnn_infer.so.8")

    except OSError:
        logger.warning("Unable to find Python cuDNN binaries, falling back to system binaries..")

    try:
        if name == "nt":
            CDLL(cublas_path / "bin" / "cublas64_12.dll")

        else:
            CDLL(cublas_path / "lib" / "libcublas.so.12")

    except OSError:
        logger.warning("Unable to find Python cuBLAS binaries, falling back to system binaries..")


def main() -> None:
    if not (args := parse_args()):
        return

    options: TranscriberOptions = {"device": "cpu"}
    caption = args["caption"]
    output = args["output"]

    if args["threads"]:
        options["number_of_threads"] = args["threads"]

    if args["workers"]:
        options["number_of_workers"] = args["workers"]

    if args["cuda"]:
        options["device"] = "cuda"
        resolve_cuda_libraries()

    if not (transcription := Transcriber(**options).transcribe(args["file"])):
        raise InvalidFileFormatError(args["file"])

    if caption == "srt":
        result = segments_to_srt(transcription)

    elif caption == "vtt":
        result = segments_to_vtt(transcription)

    else:
        result = (segment.text for segment in transcription)

    if output:
        with Path(output).open("w") as file:
            file.write("\n\n".join(result))

    else:
        with stdout as out:
            out.writelines(result)
