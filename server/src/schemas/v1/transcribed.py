from typing import Annotated

from msgspec import Meta, Struct


class Transcribed(Struct, kw_only=True, frozen=True, gc=False):
    result: Annotated[str, Meta(examples=["1\n00:00:00,000 --> 00:00:02,000\nHello world."])]
