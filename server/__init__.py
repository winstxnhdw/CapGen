from litestar import Litestar, Response
from litestar.openapi import OpenAPIConfig
from litestar.openapi.spec import Server
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR
from picologging import getLogger

from server.api import v1
from server.config import Config
from server.lifespans import load_model
from server.singleton import singleton


def exception_handler(_, exception: Exception) -> Response[dict[str, str]]:
    """
    Summary
    -------
    the Litestar exception handler

    Parameters
    ----------
    request (Request) : the request
    exception (Exception) : the exception
    """
    getLogger('custom.access').error('Application Exception', exc_info=exception)

    return Response(
        content={'detail': 'Internal Server Error'},
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )


@singleton
def app() -> Litestar:
    """
    Summary
    -------
    the Litestar application
    """
    return Litestar(
        openapi_config=OpenAPIConfig(title='CapGen', version='1.0.0', servers=[Server(url=Config.server_root_path)]),
        exception_handlers={HTTP_500_INTERNAL_SERVER_ERROR: exception_handler},
        route_handlers=[v1],
        lifespan=[load_model],
    )
