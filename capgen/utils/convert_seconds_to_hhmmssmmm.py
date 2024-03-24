def convert_seconds_to_hhmmssmmm(seconds: float, millisecond_separator: str) -> str:
    """
    Summary
    -------
    converts seconds to hh:mm:ss,mmm format

    Parameters
    ----------
    seconds (float) : the number of seconds to convert

    Returns
    -------
    converted_time (str) : the converted time in hh:mm:ss,mmm format
    """
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((seconds % 1) * 1000)

    return f'{int(hours):02}:{int(minutes):02}:{int(seconds):02}{millisecond_separator}{milliseconds:03}'
