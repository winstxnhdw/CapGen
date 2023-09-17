from typing import Literal, TypedDict


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
    num_workers: int
    compute_type: Literal[
        'default',
        'auto',
        'int8',
        'int8_float32',
        'int8_float16',
        'int8_bfloat16',
        'int16'
        'float16',
        'bfloat16',
        'float32',
    ]
