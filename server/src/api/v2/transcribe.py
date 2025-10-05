from asyncio import wrap_future
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from typing import Annotated

from litestar import Controller, post
from litestar.concurrency import _State as ConcurrencyState
from litestar.datastructures import UploadFile
from litestar.enums import RequestEncodingType
from litestar.exceptions import ClientException
from litestar.params import Body
from litestar.response.sse import ServerSentEvent
from litestar.status_codes import HTTP_200_OK

from captions import segments_to_srt, segments_to_vtt
from src.schemas.v1 import Transcribed
from src.typedefs import AppState, CaptionFormat


class TranscriptionError(ClientException):
    def __init__(self, file_name: str) -> None:
        super().__init__(detail=f"{file_name} is not a valid file!")


class TranscriberController(Controller):
    path = "/transcription"

    @post(status_code=HTTP_200_OK)
    async def transcribe(
        self,
        state: AppState,
        data: Annotated[UploadFile, Body(media_type=RequestEncodingType.MULTI_PART)],
        caption_format: CaptionFormat = "srt",
    ) -> Transcribed:
        thread_pool = ConcurrencyState.EXECUTOR or ThreadPoolExecutor()
        audio = BytesIO(await data.read())

        if not (transcription := await wrap_future(thread_pool.submit(state.transcriber.transcribe, audio))):
            raise TranscriptionError(data.filename)

        if caption_format == "srt":
            result = segments_to_srt(transcription)

        elif caption_format == "vtt":
            result = segments_to_vtt(transcription)

        else:
            result = (segment.text for segment in transcription)

        return Transcribed(result="".join(result))

    @post("/stream", status_code=HTTP_200_OK)
    async def transcribe_stream(
        self,
        state: AppState,
        data: Annotated[UploadFile, Body(media_type=RequestEncodingType.MULTI_PART)],
        caption_format: CaptionFormat = "srt",
    ) -> ServerSentEvent:
        thread_pool = ConcurrencyState.EXECUTOR or ThreadPoolExecutor()
        audio = BytesIO(await data.read())

        if not (transcription := await wrap_future(thread_pool.submit(state.transcriber.transcribe, audio))):
            raise TranscriptionError(data.filename)

        if caption_format == "srt":
            result = segments_to_srt(transcription)

        elif caption_format == "vtt":
            result = segments_to_vtt(transcription)

        else:
            result = (segment.text for segment in transcription)

        return ServerSentEvent(result)
