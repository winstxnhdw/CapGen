from typing import Literal

from fastapi import UploadFile
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from server.api.v1 import v1
from server.features import Transcriber
from server.schemas.v1 import Transcribed


@v1.post('/transcribe', response_model=Transcribed)
async def transcribe(request: UploadFile, transcription_type: Literal['srt'] = 'srt'):
    """
    Summary
    -------
    the `/transcribe` route transcribes the audio file into a chosen caption file
    """
    try:
        request.file.fileno()
        result = Transcriber.transcribe(request.file, transcription_type)

    except KeyError as exception:
        raise HTTPException(HTTP_400_BAD_REQUEST, f'Invalid transcription type: {transcription_type}!') from exception

    return Transcribed(result=result)
