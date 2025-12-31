# ruff: noqa: S101

from __future__ import annotations

from litestar import Litestar
from litestar.testing import AsyncTestClient
from pytest import mark


async def transcribe(session_client: AsyncTestClient[Litestar], audio_file: bytes, caption_format: str) -> str | None:
    response = await session_client.post(
        "/v2/transcription",
        files={"request": audio_file},
        params={"caption_format": caption_format},
    )

    return response.json().get("result")


@mark.anyio
async def test_transcribe_incorrect_format(session_client: AsyncTestClient[Litestar], audio_file: bytes) -> None:
    assert not await transcribe(session_client, audio_file, "art")


@mark.anyio
async def test_transcribe_txt(session_client: AsyncTestClient[Litestar], audio_file: bytes) -> None:
    assert await transcribe(session_client, audio_file, "txt") == "Hello there, my name is Bella."


@mark.flaky
@mark.anyio
async def test_transcribe_srt(session_client: AsyncTestClient[Litestar], audio_file: bytes) -> None:
    assert await transcribe(session_client, audio_file, "srt") in {
        "1\n00:00:00,000 --> 00:00:01,700\nHello there, my name is Bella.\n\n",
        "1\n00:00:00,000 --> 00:00:01,720\nHello there, my name is Bella.\n\n",
    }


@mark.flaky
@mark.anyio
async def test_transcribe_vtt(session_client: AsyncTestClient[Litestar], audio_file: bytes) -> None:
    assert await transcribe(session_client, audio_file, "vtt") in {
        "WEBVTT\n\n00:00:00.000 --> 00:00:01.700\nHello there, my name is Bella.\n\n",
        "WEBVTT\n\n00:00:00.000 --> 00:00:01.720\nHello there, my name is Bella.\n\n",
    }
