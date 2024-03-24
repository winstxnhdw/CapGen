# pylint: disable=missing-function-docstring,redefined-outer-name

from typing import Generator

from fastapi.testclient import TestClient
from pytest import fixture

from server import initialise


@fixture()
def client() -> Generator[TestClient, None, None]:
    with TestClient(initialise()) as client:
        yield client


def test_transcribe_srt(client: TestClient):
    with open('tests/test.mp3', 'rb') as file:
        response = client.post(
            '/v1/transcribe',
            files={ 'request': file },
            params={ 'caption_format': 'srt' }
        ).json()

    assert response['result'] == '1\n00:00:00,000 --> 00:00:02,000\nHello there. My name is Bella.'


def test_transcribe_vtt(client: TestClient):
    with open('tests/test.mp3', 'rb') as file:
        response = client.post(
            '/v1/transcribe',
            files={ 'request': file },
            params={ 'caption_format': 'vtt' }
        ).json()

    assert response['result'] == 'WEBVTT\n\n00:00:00.000 --> 00:00:02.000\nHello there. My name is Bella.'
