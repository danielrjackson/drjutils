"""
# unset.py

## drjutils.common.types

## Summary

This module provides utility functions and type aliases for working with generic types,
and setting names and docstrings for objects.

## Type Aliases

- `T`: Type variable for generic objects.

## Methods:

- `set_name`: Set the name of an object if it has a `__name__` attribute.
- `set_name_if`: Conditionally set the name of an object if it has a `__name__` attribute.
- `set_docstring`: Set the docstring of an object if it has a `__doc__` attribute.
- `set_docstring_if`: Conditionally set the docstring of an object if it has a `__doc__` attribute.
- `set_name_and_doc`: Set both the name and docstring of an object if applicable.
- `set_name_and_doc_if`: Conditionally set the name and docstring of an object.

Copyright 2025 Daniel Robert Jackson
"""

"""
Standard Libraries
"""
from typing import Callable, Final, Optional
from typing_extensions import TypeVar

__all__ = [
    "T",
    "set_name",
    "set_name_if",
    "set_docstring",
    "set_docstring_if",
    "set_name_and_doc",
    "set_name_and_doc_if",
]


UNSET: Final = object()
T = TypeVar("T")
R = TypeVar("R")

def resolved(
    value:   T | object,
    default: R | Callable[[], R]
    ) -> T | R:
    return default() if value is UNSET and callable(default) else \
           default  if value is UNSET else \
           value

T = TypeVar("T", bound=object)
"""Type variable for generic objects."""

def set_debug_name(
    obj:        T,
    debug_name: str,
    condition:  Optional[bool] = True,
    ) -> T:
    """
    Set the debug name of an object.

    This is useful for debugging and logging purposes.

    Args:
        obj:        The object to set the debug name for
        debug_name: Debug name to set for the object
        condition:  Optional condition to determine if the debug name should be set

    Returns:
        The object with the debug name set, if applicable.
    """
    if condition:
        obj._debug_name = debug_name
    return obj

def set_debug_context(
    obj:       T,
    debug_ctx: str,
    condition: Optional[bool] = True,
    ) -> T:
    """
    Set the debug context of an object.

    This is useful for debugging and logging purposes.

    Args:
        obj:       The object to set the debug context for
        debug_ctx: Debug context to set for the object
        condition: Optional condition to determine if the debug context should be set

    Returns:
        The object with the debug context set, if applicable.
    """
    if condition:
        obj._debug_context = debug_ctx
    return obj

def set_debug_name_and_context(
    obj:        T,
    debug_name: Optional[str]  = Unini,
    context:    Optional[str]  = None,
    condition:  Optional[bool] = True,
    ) -> T:
    """
    Set both the debug name and context of an object.

    This is useful for debugging and logging purposes.

    Args:
        obj:        The object to set the debug name and context for
        debug_name: Optional debug name to set for the object
        context:    Optional debug context to set for the object
        condition:  Optional condition to determine if the debug name and context should be set

    Returns:
        The object with the debug name and context set, if applicable.
    """
    if condition:
        if debug_name is not None:
            obj._debug_name = debug_name
        if context is not None:
            obj._debug_context = context


