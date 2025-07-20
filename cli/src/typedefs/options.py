from typing import Literal, TypedDict


class TranscriberOptions(TypedDict, total=False):
    device: Literal['auto', 'cpu', 'cuda']
    number_of_threads: int
    number_of_workers: int
