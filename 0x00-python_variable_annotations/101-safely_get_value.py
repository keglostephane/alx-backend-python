#!/usr/bin/env python3
"""safely_get_value module
"""
from typing import Union, Any, Mapping, TypeVar, Optional


Custom = TypeVar('T', bound=(None))


def safely_get_value(dct: Mapping,
                     key: Any,
                     default: Optional[Union[Custom, None]] = None
                     ) -> Union[Any, Custom]:
    """Safely get a value from a dictionnary"""
    if key in dct:
        return dct[key]
    else:
        return default
