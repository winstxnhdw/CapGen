from litestar.datastructures import State

from capgen.transcriber.protocol import TranscriberProtocol


class AppState(State):
    """
    Summary
    -------
    the Litestar application state that will be injected into the routers
    """

    transcriber: TranscriberProtocol
