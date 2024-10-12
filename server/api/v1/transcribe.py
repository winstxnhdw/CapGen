from io import BytesIO
from typing import Annotated

from litestar import Controller, post
from litestar.concurrency import _run_sync_asyncio as run_sync
from litestar.datastructures import UploadFile
from litestar.enums import RequestEncodingType
from litestar.exceptions import ClientException
from litestar.params import Body
from litestar.response.sse import ServerSentEvent
from litestar.status_codes import HTTP_200_OK

from capgen.transcriber import CaptionFormat
from server.schemas.v1 import Transcribed
from server.state import AppState


class TranscriberController(Controller):
    """
    Summary
    -------
    the `/transcribe` route ingests an audio file and transcribes it into a chosen caption format
    """

    path = '/transcribe'

    @post(status_code=HTTP_200_OK)
    async def transcribe(
        self,
        state: AppState,
        data: Annotated[UploadFile, Body(media_type=RequestEncodingType.MULTI_PART)],
        caption_format: CaptionFormat = 'srt',
    ) -> Transcribed:
        """
        Summary
        -------
        the POST variant of the `/transcribe` route
        """
        audio = BytesIO(await data.read())
        transcription = await run_sync(state.transcriber.transcribe, audio, caption_format)

        if not transcription:
            raise ClientException(detail=f'Invalid file: {data.filename}!')

        return Transcribed(result='\n\n'.join(transcription))

    @post('/stream', status_code=HTTP_200_OK)
    async def transcribe_stream(
        self,
        state: AppState,
        data: Annotated[UploadFile, Body(media_type=RequestEncodingType.MULTI_PART)],
        caption_format: CaptionFormat = 'srt',
    ) -> ServerSentEvent:
        """
        Summary
        -------
        the POST variant of the `/transcribe/stream` route
        """
        audio = BytesIO(await data.read())
        transcription = await run_sync(state.transcriber.transcribe, audio, caption_format)

        if not transcription:
            raise ClientException(detail=f'Invalid file: {data.filename}!')

        return ServerSentEvent(transcription)
