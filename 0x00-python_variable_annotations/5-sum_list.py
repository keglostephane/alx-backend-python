#!/usr/bin/env python3
"""sum_list module
"""
from typing import List


def sum_list(input_list: List[float]) -> float:
    """Return the sum of float numbers"""
    return sum(input_list, 0.0)
