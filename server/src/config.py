from __future__ import annotations

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    app_name: str = 'CapGen'
    server_port: int = 49494
    server_root_path: str = '/api'
    worker_count: int = 1
    use_cuda: bool = False
    request_max_body_size: int = 209715200

    consul_http_addr: str | None = None
    consul_auth_token: str | None = None
    consul_service_address: str = 'winstxnhdw-capgen.hf.space'
