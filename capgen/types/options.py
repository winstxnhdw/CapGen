from typing import TypedDict


class TranscriberOptions(TypedDict):
    """
    Summary
    -------
    the options for the transcriber

    Attributes
    ----------
    model_size_or_path (str) : the model size or path
    compute_type (str) : the compute type
    num_workers (int) : the number of workers
    """
    model_size_or_path: str
    compute_type: str
    num_workers: int
