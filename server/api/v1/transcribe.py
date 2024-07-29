from io import BytesIO
from typing import Annotated, Literal

from litestar import Controller, post
from litestar.datastructures import UploadFile
from litestar.enums import RequestEncodingType
from litestar.exceptions import HTTPException
from litestar.params import Body
from litestar.status_codes import HTTP_400_BAD_REQUEST

from server.features import Transcriber
from server.schemas.v1 import Transcribed


class TranscriberController(Controller):
    """
    Summary
    -------
    the `/transcribe` route ingests an audio file and transcribes it into a chosen caption format
    """

    path = '/transcribe'

    @post()
    async def transcribe(
        self,
        data: Annotated[UploadFile, Body(media_type=RequestEncodingType.MULTI_PART)],
        caption_format: Literal['srt', 'vtt'] = 'srt',
    ) -> Transcribed:
        """
        Summary
        -------
        the POST variant of the `/transcribe` route
        """
        if not (result := await Transcriber.transcribe(BytesIO(await data.read()), caption_format)):
            raise HTTPException(detail=f'Invalid format: {caption_format}!', status_code=HTTP_400_BAD_REQUEST)

        return Transcribed(result=result)
