#!/usr/bin/env python3
"""element_length module
"""
from typing import List, Iterable, Sequence, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """Return a list of tuples (value, length)"""
    return [(i, len(i)) for i in lst]
