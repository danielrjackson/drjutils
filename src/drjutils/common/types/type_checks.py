"""
# type_checks.py

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
from typing import Optional
from collections.abc import Collection
from typing_extensions import TypeAlias, TypeVar

"""
Package Libraries
"""
# These utilities provide simple helpers for assigning names and docstrings
# to objects at runtime. They intentionally do not rely on any additional
# modules so that this file can stand on its own.

__all__ = [
    "T",
    "Many",
    "set_name",
    "set_name_if",
    "set_docstring",
    "set_docstring_if",
    "set_name_and_doc",
    "set_name_and_doc_if",
]

T = TypeVar("T")
"""Type variable for generic objects."""

Many: TypeAlias = Collection[T]

def set_name(
    obj:  T,
    name: str,
    ) -> T:
    """
    Set the name of an object if it has a `__name__` attribute.
    This is useful for debugging and logging purposes.

    Args:
        obj:  The object to set the name for
        name: Name to set for the object

    Returns:
        The object with the name set, if applicable.
    """
    if hasattr(obj, "__name__") and name is not None:
        obj.__name__ = name
    return obj

def set_name_if(
    obj:       T,
    condition: bool          = True,
    name:      Optional[str] = None,
    ) -> T:
    """
    Conditionally set the name of an object if it has a `__name__` attribute.

    Args:
        obj:       The object to set the name for
        condition: Condition to determine if the name should be set
        name:      Name to set for the object (optional)

    Returns:
        The object with the name set, if applicable.
    """
    return set_name(obj, name) if condition else obj

def set_docstring(
    obj: T,
    doc: str,
    ) -> T:
    """
    Set the docstring of an object if it has a `__doc__` attribute.
    This is useful for documentation purposes.

    Args:
        obj: The object to set the docstring for
        doc: Docstring to set for the object

    Returns:
        The object with the docstring set, if applicable.
    """
    if hasattr(obj, "__doc__") and doc is not None:
        obj.__doc__ = doc
    return obj

def set_docstring_if(
    obj:       T,
    condition: bool          = True,
    doc:       Optional[str] = None,
    ) -> T:
    """
    Conditionally set the docstring of an object if it has a `__doc__` attribute.

    Args:
        obj:       The object to set the docstring for
        condition: Condition to determine if the docstring should be set
        doc:       Docstring to set for the object (optional)

    Returns:
        The object with the docstring set, if applicable.
    """
    return set_docstring(obj, doc) if condition else obj

def set_name_and_doc(
    obj:  T,
    name: Optional[str] = None,
    doc:  Optional[str] = None,
    ) -> T:
    """
    Set both the name and docstring of an object if applicable.

    Args:
        obj:  The object to set the name and docstring for
        name: Name to set for the object (optional)
        doc:  Docstring to set for the object (optional)

    Returns:
        The object with the name and docstring set, if applicable.
    """
    return set_docstring(set_name(obj, name), doc)

def set_name_and_doc_if(
    obj:       T,
    condition: bool          = True,
    name:      Optional[str] = None,
    doc:       Optional[str] = None,
    ) -> T:
    """
    Conditionally set the name and docstring of an object.

    Args:
        obj:       The object to set the name and docstring for
        condition: Condition to determine if the name and docstring should be set
        name:      Name to set for the object (optional)
        doc:       Docstring to set for the object (optional)

    Returns:
        The object with the name and docstring set, if applicable.
    """
    return set_name_and_doc(obj, name, doc) if condition else obj
