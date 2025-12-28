from functools import partial
from logging import Logger, getLogger
from random import choice
from string import ascii_letters, digits

from litestar import Litestar, Response, Router
from litestar.contrib.opentelemetry import OpenTelemetryConfig, OpenTelemetryPlugin
from litestar.openapi import OpenAPIConfig
from litestar.openapi.spec import Server
from litestar.plugins import PluginProtocol
from litestar.plugins.prometheus import PrometheusConfig, PrometheusController
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR

from src.api import health
from src.api.v2 import TranscriberController
from src.config import Config
from src.lifespans import load_transcriber_model
from src.plugins import ConsulPlugin
from src.telemetry import get_log_handler, get_meter_provider, get_tracer_provider


def exception_handler(logger: Logger, _, exception: Exception) -> Response[dict[str, str]]:
    logger.error(exception, exc_info=exception)

    return Response(
        content={"detail": "Internal Server Error"},
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )


def app() -> Litestar:
    config = Config()
    ascii_letters_with_digits = f"{ascii_letters}{digits}"
    app_name = config.app_name
    app_id = f"{app_name}-{''.join(choice(ascii_letters_with_digits) for _ in range(4))}"  # noqa: S311
    logger = getLogger(app_name)
    plugins: list[PluginProtocol] = []

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

    if config.otel_exporter_otlp_endpoint:
        handler = get_log_handler(otlp_service_name=app_name, otlp_service_instance_id=app_id)
        logger.addHandler(handler)
        getLogger("granian.access").addHandler(handler)
        opentelemetry_config = OpenTelemetryConfig(
            tracer_provider=get_tracer_provider(otlp_service_name=app_name, otlp_service_instance_id=app_id),
            meter_provider=get_meter_provider(otlp_service_name=app_name, otlp_service_instance_id=app_id),
        )

        plugins.append(OpenTelemetryPlugin(opentelemetry_config))

    if config.consul_http_addr and config.consul_service_address:
        consul_plugin = ConsulPlugin(
            app_name=app_name,
            app_id=app_id,
            consul_http_addr=config.consul_http_addr,
            consul_service_address=config.consul_service_address,
            server_root_path=config.server_root_path,
            consul_auth_token=config.consul_auth_token,
        )

        plugins.append(consul_plugin)

    return Litestar(
        openapi_config=openapi_config,
        exception_handlers={HTTP_500_INTERNAL_SERVER_ERROR: partial(exception_handler, logger)},
        route_handlers=[PrometheusController, v2_router, health],
        plugins=plugins,
        lifespan=[load_transcriber_model(logger=logger, use_cuda=config.use_cuda, worker_count=config.worker_count)],
        middleware=[PrometheusConfig(app_name).middleware],
        request_max_body_size=config.request_max_body_size,
    )
