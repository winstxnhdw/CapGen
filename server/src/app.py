from functools import partial
from logging import Logger, getLogger

from litestar import Litestar, Response, Router
from litestar.datastructures import State
from litestar.openapi import OpenAPIConfig
from litestar.openapi.spec import Server
from litestar.plugins.prometheus import PrometheusConfig, PrometheusController
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR

from src.api import health
from src.api.v2 import TranscriberController
from src.config import Config
from src.lifespans import consul_register, load_model


def exception_handler(
    logger: Logger, _, exception: Exception
) -> Response[dict[str, str]]:
    error_message = "Internal Server Error"
    logger.error(error_message, exc_info=exception)

    return Response(
        content={"detail": error_message},
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )


def app() -> Litestar:
    config = Config()
    app_name = config.app_name
    logger = getLogger(app_name)

    openapi_config = OpenAPIConfig(
        title=app_name,
        version="1.0.0",
        description="A fast CPU-based transcriber API",
        servers=[Server(url=config.server_root_path)],
    )

    v2_router = Router(
        "/v2",
        tags=["v2"],
        route_handlers=[TranscriberController],
    )

    return Litestar(
        openapi_config=openapi_config,
        exception_handlers={
            HTTP_500_INTERNAL_SERVER_ERROR: partial(exception_handler, logger)
        },
        route_handlers=[PrometheusController, v2_router, health],
        lifespan=[consul_register, load_model],
        middleware=[PrometheusConfig(app_name).middleware],
        request_max_body_size=config.request_max_body_size,
        state=State({"config": config}),
    )
