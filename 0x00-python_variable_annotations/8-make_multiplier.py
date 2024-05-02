#!/usr/bin/env python3
"""make_multiplier module"""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """Return a function that multiply a float by a number."""
    def multiply(num: float):
        """Multiply two numbers."""
        return num * multiplier
    return multiply
