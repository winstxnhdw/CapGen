# pylint: disable=missing-function-docstring,redefined-outer-name


from litestar import Litestar
from litestar.testing import AsyncTestClient


async def test_transcribe_srt(client: AsyncTestClient[Litestar]):
    with open('tests/test.mp3', 'rb') as file:
        response = await client.post('/v1/transcribe', files={'request': file}, params={'caption_format': 'srt'})

    assert response.json()['result'] == '1\n00:00:00,000 --> 00:00:01,720\nHello there, my name is Bella.'


async def test_transcribe_vtt(client: AsyncTestClient[Litestar]):
    with open('tests/test.mp3', 'rb') as file:
        response = await client.post('/v1/transcribe', files={'request': file}, params={'caption_format': 'vtt'})

    assert response.json()['result'] == 'WEBVTT\n\n00:00:00.000 --> 00:00:01.720\nHello there, my name is Bella.'
