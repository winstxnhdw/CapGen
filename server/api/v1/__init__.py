from litestar import Router

from server.api.v1.index import index
from server.api.v1.transcribe import TranscriberController

v1 = Router('/v1', tags=['v1'], route_handlers=[index, TranscriberController])
