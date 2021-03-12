def parse_int(s: str):
    """
    returns the number if is convertible to int, None otherwise

    :param s: str
    :return: int or None
    """

    try:
        return int(s)
    except ValueError:
        return None


def parse_bool(s: str):
    """
    returns a bool if convertible, None otherwise

    :param s: str
    :return: bool or None
    """
    if s.lower() in ["off", "false", "no"]:
        return False
    elif s.lower() in ["on", "true", "yes"]:
        return True

    return None
