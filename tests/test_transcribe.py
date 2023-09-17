# pylint: disable=missing-function-docstring,redefined-outer-name

from fastapi.testclient import TestClient
from pytest import fixture

from server import initialise


@fixture()
def client():
    return TestClient(initialise())


def test_transcribe(client: TestClient):
    with open('tests/test.mp3', 'rb') as file:
        response = client.post(
            '/v1/transcribe',
            files={ 'request': file },
            params={ 'caption_format': 'srt' }
        ).json()

    assert response['result'] == '1\n00:00:00,000 --> 00:00:02,000\nHello there, my name is Bella.'
