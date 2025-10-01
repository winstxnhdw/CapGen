from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from random import choice
from string import ascii_letters, digits

from aiohttp import ClientSession

from src.api import health
from src.lifespans.inject_state import inject_state
from src.typedefs import AppState


@inject_state
@asynccontextmanager
async def consul_register(_, state: AppState) -> AsyncIterator[None]:
    config = state.config

    if not config.consul_http_addr:
        yield
        return

    consul_server = f"https://{config.consul_http_addr}/v1/agent/service"
    health_check = {
        "HTTP": f"https://{config.consul_service_address}{config.server_root_path}{health.paths.pop()}",
        "Interval": "10s",
        "Timeout": "5s",
    }

    ascii_letters_with_digits = f"{ascii_letters}{digits}"
    payload = {
        "Name": config.app_name,
        "ID": f"{config.app_name}-{''.join(choice(ascii_letters_with_digits) for _ in range(4))}",  # noqa: S311
        "Tags": ["prometheus"],
        "Address": config.consul_service_address,
        "Port": 443,
        "Check": health_check,
        "Meta": {
            "metrics_port": "443",
            "metrics_path": "/metrics",
        },
    }

    async with ClientSession(
        headers={"Authorization": f"Bearer {config.consul_auth_token}"}
    ) as session:
        async with session.put(
            f"{consul_server}/register",
            json=payload,
            params={"replace-existing-checks": "true"},
        ) as response:
            response.raise_for_status()

        try:
            yield

        finally:
            async with session.put(f"{consul_server}/deregister/{payload['ID']}"):
                pass
