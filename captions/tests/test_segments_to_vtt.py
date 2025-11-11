# ruff: noqa: S101


from conftest import Segment

from captions import segments_to_vtt


def test_segments_to_vtt(segments: tuple[Segment, ...]) -> None:
    assert tuple(segments_to_vtt(segments)) == (
        "WEBVTT\n\n",
        "00:00:00.000 --> 00:00:01.720\nHello there, my name is Bella.\n\n",
        "00:00:02.000 --> 00:00:04.500\nWelcome to the captions library.\n\n",
    )
