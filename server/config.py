from typing import Callable

from pydantic_settings import BaseSettings


def singleton[T](callable_object: Callable[[], T]) -> T:
    """
    Summary
    -------
    a decorator to transform a callable/class to a singleton

    Parameters
    ----------
    callable_object (Callable[[], T]) : the callable to transform

    Returns
    -------
    instance (T) : the singleton
    """
    return callable_object()


@singleton
class Config(BaseSettings):
    """
    Summary
    -------
    the general config class

    Attributes
    ----------
    port (int) : the port to run the server on
    server_root_path (str) : the root path for the server
    worker_count (int) : the number of workers to use
    use_cuda (bool) : whether to use CUDA for inference
    transcriber_model_name (str) : the name of the transcriber model to use
    """

    server_port: int = 49494
    server_root_path: str = '/api'
    worker_count: int = 1
    use_cuda: bool = False
    transcriber_model_name: str = 'facebook/wav2vec2-base-960h'
