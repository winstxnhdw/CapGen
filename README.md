# CapGen

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)
[![main.yml](https://github.com/winstxnhdw/CapGen/actions/workflows/main.yml/badge.svg)](https://github.com/winstxnhdw/CapGen/actions/workflows/main.yml)
[![build.yml](https://github.com/winstxnhdw/CapGen/actions/workflows/build.yml/badge.svg)](https://github.com/winstxnhdw/CapGen/actions/workflows/build.yml)
[![formatter.yml](https://github.com/winstxnhdw/CapGen/actions/workflows/formatter.yml/badge.svg)](https://github.com/winstxnhdw/CapGen/actions/workflows/formatter.yml)
[![warmer.yml](https://github.com/winstxnhdw/CapGen/actions/workflows/warmer.yml/badge.svg)](https://github.com/winstxnhdw/CapGen/actions/workflows/warmer.yml)
[![dependabot.yml](https://github.com/winstxnhdw/CapGen/actions/workflows/dependabot.yml/badge.svg)](https://github.com/winstxnhdw/CapGen/actions/workflows/dependabot.yml)

[![Open in Spaces](https://huggingface.co/datasets/huggingface/badges/raw/main/open-in-hf-spaces-md-dark.svg)](https://huggingface.co/spaces/winstxnhdw/CapGen)
[![Open a Pull Request](https://huggingface.co/datasets/huggingface/badges/raw/main/open-a-pr-md-dark.svg)](https://github.com/winstxnhdw/CapGen/compare)

A video/audio transcriber for generating caption files with Whisper and CTranslate2.

## Usage (API)

Simply cURL the endpoint like in the following. Currently, the only available transcription type is `srt`.

```bash
curl 'https://winstxnhdw-CapGen.hf.space/v1/transcribe?transcription_type=$TRANSCRIPTION_TYPE' \
  -H 'Content-Type: multipart/form-data' \
  -F 'request=@$AUDIO_FILE_PATH;type=audio/mpeg'
```

You can also redirect the output to a file.

```bash
curl 'https://winstxnhdw-CapGen.hf.space/v1/transcribe?transcription_type=srt' \
  -H 'Content-Type: multipart/form-data' \
  -F 'request=@$AUDIO_FILE_PATH;type=audio/mpeg' | jq '.result' > $OUTPUT_DIRECTORY/result.srt
```

## Usage (CLI)

Install the necessary dependencies with `poetry`.

```bash
poetry install --without=server
```

You can run the transcriber as a CLI tool.

```bash
python transcribe.py -f ~/Downloads/audio.mp3 -t srt -o ./result.srt
```

```yaml
usage: transcribe.py [-h] -f  -t  -o

Transcribe a compatible audio/video file into a chosen caption file

options:
  -h, --help     show this help message and exit
  -f, --file     the file path to a compatible audio/video
  -t, --type     the chosen caption file format
  -o, --output   the output file path
```
