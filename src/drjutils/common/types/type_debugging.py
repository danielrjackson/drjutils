"""
# type_debugging.py

## drjutils.common.types

## Summary

This module provides utility functions and type aliases for working with generic types,
and setting names and docstrings for objects.

## Type Aliases

- `T`: Type variable for generic objects.

## Methods:

- `set_debug_name`: Set the debug name of an object if it has a `_debug_name` attribute.
- `set_debug_context`: Conditionally set the name of an object if it has a `__name__` attribute.
- `set_debug_name_and_context`: Set the docstring of an object if it has a `__doc__` attribute.
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

from drjutils.common.types.sentinel import Opt, OptOrNone, OrNone, UNSET, resolve

resolve()

__all__ = [
    "_T",
    "set_debug_name",
    "set_debug_context",
    "set_debug_name_and_context",
]


_T = TypeVar("T")
_R = TypeVar("R")

def set_debug_name(
    obj:        _T,
    debug_name: OptOrNone[str] = UNSET,
    condition:  OrNone[bool]   = None,
    ) -> _T:
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
    assert obj, "Object must not be None to set a debug name."
    assert debug_name is not UNSET, "Debug name must be provided to set a debug name."
    if condition:
        obj._debug_name = debug_name
    return obj

def set_debug_context(
    obj:       _T,
    debug_ctx: OptOrNone[str] = UNSET,
    condition: OrNone[bool]   = None,
    ) -> _T:
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
    assert obj, "Object must not be None to set a debug context."
    if condition:
        obj._debug_context = debug_ctx
    return obj

def set_debug_name_and_context(
    obj:        _T,
    /, *,
    debug_name: OptOrNone[str]  = UNSET,
    context:    OptOrNone[str]  = UNSET,
    condition:  OrNone[bool]    = None,
    ) -> _T:
    """
    Set both the debug name and context of an object.

    This is useful for debugging and logging purposes.

    At least one of debug_name or context must be provided.

    Args:
        obj:        The object to set the debug name and context for
        debug_name: Optional debug name to set for the object
        context:    Optional debug context to set for the object
        condition:  Optional condition to determine if the debug name and context should be set

    Returns:
        The object with the debug name and context set, if applicable.
    """
    assert obj, "Object must not be None to set a debug name and/or context."
    assert debug_name is not UNSET or context is not UNSET, "At least one of debug_name or context \
        must be provided."
    if condition:
        if debug_name is not UNSET:
            obj._debug_name    = debug_name
        if context    is not UNSET:
            obj._debug_context = context