from litestar.datastructures import State

from capgen.transcriber.protocol import TranscriberProtocol


class AppState(State):
    """
    Summary
    -------
    the Litestar application state that will be injected into the routers

    Attributes
    ----------
    transcriber (TranscriberProtocol) : the transcriber instance for transcribing audio
    """

    transcriber: TranscriberProtocol
