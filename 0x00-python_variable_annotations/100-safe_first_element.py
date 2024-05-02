#!/usr/bin/env python3
"""safe_first_element module
"""
from typing import Sequence, Any, Union


# The types of the elements of the input are not know
def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """Return the first value of sequence or None"""
    if lst:
        return lst[0]
    else:
        return None
