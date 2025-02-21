from typing import Annotated

from msgspec import Meta, Struct


class Transcribed(Struct):
    """
    Summary
    -------
    the transcribed schema

    Attributes
    ----------
    result (str) : the transcribed text in the chosen caption file format
    """

    result: Annotated[str, Meta(examples=['1\n00:00:00,000 --> 00:00:02,000\nHello world.'])]
