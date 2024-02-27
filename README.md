# CapGen

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)
[![deploy.yml](https://github.com/winstxnhdw/CapGen/actions/workflows/deploy.yml/badge.svg)](https://github.com/winstxnhdw/CapGen/actions/workflows/deploy.yml)
[![build.yml](https://github.com/winstxnhdw/CapGen/actions/workflows/build.yml/badge.svg)](https://github.com/winstxnhdw/CapGen/actions/workflows/build.yml)
[![formatter.yml](https://github.com/winstxnhdw/CapGen/actions/workflows/formatter.yml/badge.svg)](https://github.com/winstxnhdw/CapGen/actions/workflows/formatter.yml)
[![warmer.yml](https://github.com/winstxnhdw/CapGen/actions/workflows/warmer.yml/badge.svg)](https://github.com/winstxnhdw/CapGen/actions/workflows/warmer.yml)
[![dependabot.yml](https://github.com/winstxnhdw/CapGen/actions/workflows/dependabot.yml/badge.svg)](https://github.com/winstxnhdw/CapGen/actions/workflows/dependabot.yml)

[![Open in Spaces](https://huggingface.co/datasets/huggingface/badges/raw/main/open-in-hf-spaces-md-dark.svg)](https://huggingface.co/spaces/winstxnhdw/CapGen)
[![Open a Pull Request](https://huggingface.co/datasets/huggingface/badges/raw/main/open-a-pr-md-dark.svg)](https://github.com/winstxnhdw/CapGen/compare)

A fast CPU-first video/audio transcriber for generating caption files with [Whisper](https://openai.com/research/whisper) and [CTranslate2](https://github.com/OpenNMT/CTranslate2), hosted on Hugging Face Spaces. A `pip` installable offline CLI tool with CUDA support is provided. By default, Voice Activity Detection (VAD) preprocessing is always enabled.

## Requirements

- Python 3.11

## Usage (API)

Simply cURL the endpoint like in the following. Currently, the only available caption format is `srt`.

```bash
curl "https://winstxnhdw-CapGen.hf.space/api/v1/transcribe?caption_format=$CAPTION_FORMAT" \
  -F "request=@$AUDIO_FILE_PATH"
```

You can also redirect the output to a file.

```bash
  curl "https://winstxnhdw-CapGen.hf.space/api/v1/transcribe" \
    -F "request=@$AUDIO_FILE_PATH" | jq -r ".result" > result.srt
```

## Usage (CLI)

`CapGen` is available as a CLI tool with CUDA support. You can install it with `pip`.

```bash
pip install git+https://github.com/winstxnhdw/CapGen
```

You may also install `CapGen` with the necessary CUDA binaries.

```bash
pip install 'capgen[cuda] @ git+https://github.com/winstxnhdw/CapGen'
```

Now, you can run the CLI tool with the following command.

```bash
capgen -c srt -o ./result.srt --cuda < ~/Downloads/audio.mp3
```

```yaml
usage: capgen [-h] [-g] [-t] [-w] -c  -o  [file]

transcribe a compatible audio/video file into a chosen caption file format

positional arguments:
  file            the file path to a compatible audio/video

options:
  -h, --help      show this help message and exit
  -g, --cuda      whether to use CUDA for inference

cpu:
  -t, --threads   the number of CPU threads
  -w, --workers   the number of CPU workers

required:
  -c, --caption   the chosen caption file format
  -o, --output    the output file path
```

## Development

You can install the required dependencies for your editor with the following.

```bash
poetry install
```

You can spin the server up locally with the following. You can access the Swagger UI at [localhost:7860/api/docs](http://localhost:7860/api/docs).

```bash
docker build -f Dockerfile.build -t capgen .
docker run --rm -e APP_PORT=7860 -p 7860:7860 capgen
```
