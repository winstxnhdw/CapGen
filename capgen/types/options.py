from typing import Literal, TypedDict


class TranscriberOptions(TypedDict, total=False):
    """
    Summary
    -------
    the options for the transcriber

    Attributes
    ----------
    device (Literal['auto', 'cpu', 'cuda']) : the device to use for inference
    number_of_threads (int) : the number of CPU threads
    number_of_workers (int) : the number of workers
    """

    device: Literal['auto', 'cpu', 'cuda']
    number_of_threads: int
    number_of_workers: int
