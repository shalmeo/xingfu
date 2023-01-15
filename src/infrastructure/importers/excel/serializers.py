from typing import Any


def serialize(value: Any):
    if value is None:
        return value

    if isinstance(value, (str, int, dict, list)):
        return value

    return str(value)
