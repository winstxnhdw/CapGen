from pydantic import BaseModel, Field


class Transcribed(BaseModel):
    """
    Summary
    -------
    the transcribed schema

    Attributes
    ----------
    result (str) : the transcribed text in the chosen caption file format
    """

    result: str = Field(examples=['1\n' '00:00:00,000 --> 00:00:02,000\n' 'Hello world.'])
