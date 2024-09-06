from asyncio import wrap_future
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from typing import Annotated, Literal

from litestar import Controller, post
from litestar.datastructures import UploadFile
from litestar.enums import RequestEncodingType
from litestar.exceptions import ClientException
from litestar.params import Body
from litestar.status_codes import HTTP_200_OK

from server.schemas.v1 import Transcribed
from server.state import AppState


class TranscriberController(Controller):
    """
    Summary
    -------
    the `/transcribe` route ingests an audio file and transcribes it into a chosen caption format
    """

    path = '/transcribe'
    thread_pool = ThreadPoolExecutor()

    @post(status_code=HTTP_200_OK)
    async def transcribe(
        self,
        state: AppState,
        data: Annotated[UploadFile, Body(media_type=RequestEncodingType.MULTI_PART)],
        caption_format: Literal['srt', 'vtt'] = 'srt',
    ) -> Transcribed:
        """
        Summary
        -------
        the POST variant of the `/transcribe` route
        """
        audio = BytesIO(await data.read())
        transcription = await wrap_future(self.thread_pool.submit(state.transcriber.transcribe, audio, caption_format))

        if not transcription:
            raise ClientException(detail=f'Invalid format: {caption_format}!')

        return Transcribed(result=transcription)
