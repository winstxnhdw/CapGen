from typing import Literal

from fastapi import UploadFile
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from server.api.v1 import v1
from server.features import Transcriber
from server.schemas.v1 import Transcribed


@v1.post('/transcribe', response_model=Transcribed)
async def transcribe(request: UploadFile, caption_format: Literal['srt', 'vtt'] = 'srt'):
    """
    Summary
    -------
    the `/transcribe` route transcribes the audio file into a chosen caption format
    """
    request.file.fileno()

    if not (result := await Transcriber.transcribe(request.file, caption_format)):
        raise HTTPException(HTTP_400_BAD_REQUEST, f'Invalid format: {caption_format}!')

    return Transcribed(result=result)
