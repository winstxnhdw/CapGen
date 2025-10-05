# CapGen

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![python](https://img.shields.io/badge/python-3.8%20|%203.9%20|%203.10%20|%203.11%20|%203.12%20|%203.13-blue)](https://www.python.org/)

[![main.yml](https://github.com/winstxnhdw/CapGen/actions/workflows/main.yml/badge.svg)](https://github.com/winstxnhdw/CapGen/actions/workflows/main.yml)
[![clippy.yml](https://github.com/winstxnhdw/CapGen/actions/workflows/clippy.yml/badge.svg)](https://github.com/winstxnhdw/CapGen/actions/workflows/clippy.yml)
[![deploy.yml](https://github.com/winstxnhdw/CapGen/actions/workflows/deploy.yml/badge.svg)](https://github.com/winstxnhdw/CapGen/actions/workflows/deploy.yml)
[![cli.yml](https://github.com/winstxnhdw/CapGen/actions/workflows/cli.yml/badge.svg)](https://github.com/winstxnhdw/CapGen/actions/workflows/cli.yml)
[![formatter.yml](https://github.com/winstxnhdw/CapGen/actions/workflows/formatter.yml/badge.svg)](https://github.com/winstxnhdw/CapGen/actions/workflows/formatter.yml)

[![Open in Spaces](https://huggingface.co/datasets/huggingface/badges/raw/main/open-in-hf-spaces-md-dark.svg)](https://huggingface.co/spaces/winstxnhdw/CapGen)
[![Open a Pull Request](https://huggingface.co/datasets/huggingface/badges/raw/main/open-a-pr-md-dark.svg)](https://github.com/winstxnhdw/CapGen/compare)

A fast cross-platform CPU-first video/audio English-only transcriber for generating caption files with [Whisper](https://openai.com/research/whisper) and [CTranslate2](https://github.com/OpenNMT/CTranslate2), hosted on Hugging Face Spaces. A `pip` installable offline CLI tool with CUDA support is provided. By default, Voice Activity Detection (VAD) preprocessing is always enabled.

## Usage (API)

Simply cURL the endpoint like in the following. Currently, the only available caption format are `srt`, `vtt` and `txt`.

```bash
curl "https://winstxnhdw-CapGen.hf.space/api/v2/transcribe?caption_format=$CAPTION_FORMAT" \
  -F "file=@$AUDIO_FILE_PATH"
```

You can also redirect the output to a file.

```bash
curl "https://winstxnhdw-CapGen.hf.space/api/v2/transcribe?caption_format=$CAPTION_FORMAT" \
  -F "file=@$AUDIO_FILE_PATH" | jq -r ".result" > result.srt
```

You can stream the captions in real-time with the following.

```bash
curl -N "https://winstxnhdw-CapGen.hf.space/api/v2/transcribe/stream?caption_format=$CAPTION_FORMAT" \
  -F "file=@$AUDIO_FILE_PATH"
```

## Usage (CLI)

`CapGen` is available as a CLI tool with CUDA support. You can install it with `pip`.

```bash
pip install "capgen-cli @ git+https://github.com/winstxnhdw/CapGen#subdirectory=cli"
```

You may also install `capgen` with the necessary CUDA binaries.

```bash
pip install "capgen-cli[cuda] @ git+https://github.com/winstxnhdw/CapGen#subdirectory=cli"
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
  -c, --caption   the chosen caption file format
  -o, --output    the output file path

cpu:
  -t, --threads   the number of CPU threads
  -w, --workers   the number of CPU workers
```

## Development

You can install the required dependencies for your editor with the following.

```bash
uv sync --all-packages
```

You can spin the server up locally with the following. You can access the Swagger UI at [localhost:7860/api/docs](http://localhost:7860/api/docs).

```bash
docker build -f Dockerfile.build -t capgen .
docker run --rm -e SERVER_PORT=7860 -p 7860:7860 capgen
```
