from granian.constants import Interfaces
from granian.server import Server

from src.app import app
from src.config import Config


def main() -> None:
    config = Config()

    granian = Server(
        f'{app.__module__}:{app.__name__}',
        address='0.0.0.0',  # noqa: S104
        port=config.server_port,
        interface=Interfaces.ASGI,
        workers=config.worker_count,
        log_access=True,
        log_access_format='[%(time)s] %(status)d "%(method)s %(path)s %(protocol)s" %(addr)s in %(dt_ms).2f ms',
        url_path_prefix=config.server_root_path,
        factory=True,
        reload=False,
    )

    granian.serve()
