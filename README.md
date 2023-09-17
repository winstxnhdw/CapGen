# CapGen

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)
[![main.yml](https://github.com/winstxnhdw/CapGen/actions/workflows/main.yml/badge.svg)](https://github.com/winstxnhdw/CapGen/actions/workflows/main.yml)
[![deploy.yml](https://github.com/winstxnhdw/CapGen/actions/workflows/deploy.yml/badge.svg)](https://github.com/winstxnhdw/CapGen/actions/workflows/deploy.yml)
[![build.yml](https://github.com/winstxnhdw/CapGen/actions/workflows/build.yml/badge.svg)](https://github.com/winstxnhdw/CapGen/actions/workflows/build.yml)
[![formatter.yml](https://github.com/winstxnhdw/CapGen/actions/workflows/formatter.yml/badge.svg)](https://github.com/winstxnhdw/CapGen/actions/workflows/formatter.yml)
[![warmer.yml](https://github.com/winstxnhdw/CapGen/actions/workflows/warmer.yml/badge.svg)](https://github.com/winstxnhdw/CapGen/actions/workflows/warmer.yml)
[![dependabot.yml](https://github.com/winstxnhdw/CapGen/actions/workflows/dependabot.yml/badge.svg)](https://github.com/winstxnhdw/CapGen/actions/workflows/dependabot.yml)

[![Open in Spaces](https://huggingface.co/datasets/huggingface/badges/raw/main/open-in-hf-spaces-md-dark.svg)](https://huggingface.co/spaces/winstxnhdw/CapGen)
[![Open a Pull Request](https://huggingface.co/datasets/huggingface/badges/raw/main/open-a-pr-md-dark.svg)](https://github.com/winstxnhdw/CapGen/compare)

A fast CPU-first video/audio transcriber for generating caption files with [Whisper](https://openai.com/research/whisper) and [CTranslate2](https://github.com/OpenNMT/CTranslate2), hosted on Hugging Face Spaces. Includes a local CLI tool with CUDA support.

## Requirements

- Python 3.11
- Poetry 1.5.0
- cuBLAS*
- cuDNN*

> *Only required if you are planning to run with `--cuda`

## Usage (API)

Simply cURL the endpoint like in the following. Currently, the only available caption format is `srt`.

```bash
curl "https://winstxnhdw-CapGen.hf.space/v1/transcribe?caption_format=$CAPTION_FORMAT" \
  -H "Content-Type: multipart/form-data" \
  -F "request=@$AUDIO_FILE_PATH;type=audio/mpeg"
```

You can also redirect the output to a file.

```bash
curl "https://winstxnhdw-CapGen.hf.space/v1/transcribe" \
  -H "Content-Type: multipart/form-data" \
  -F "request=@$AUDIO_FILE_PATH;type=audio/mpeg" | jq -r ".result" > $OUTPUT_DIRECTORY/result.srt
```

## Usage (CLI)

`CapGen` is available as a CLI tool with CUDA support. First, install the `CapGen` package.

```bash
pip install git+https://github.com/winstxnhdw/CapGen
```

Now, you can run the CLI tool with the following command.

```bash
capgen -f ~/Downloads/audio.mp3 -c srt -o ./result.srt --cuda
```

```yaml
usage: capgen [-h] [-g] -f  -c  -o

Transcribe a compatible audio/video file into a chosen caption file

options:
  -h, --help      show this help message and exit
  -g, --cuda      whether to use CUDA for inference

required:
  -f, --file      the file path to a compatible audio/video
  -c, --caption   the chosen caption file format
  -o, --output    the output file path
```
