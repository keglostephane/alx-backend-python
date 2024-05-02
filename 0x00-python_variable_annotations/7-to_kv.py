#!/usr/bin/env python3
"""to_kv module
"""
from typing import Tuple, Union


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """Return a tuple of string and squared number"""
    return (k, v**2)
