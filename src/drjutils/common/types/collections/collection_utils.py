"""
# collection_utils.py

## drjutils.common.types.collections

## Summary

This module provides utilities for working with collections in Python.

## Methods:

- `assert_enum_and_str_reps_exist`: Asserts that an Enum member and its string representation(s)
    exist and are not `None` or empty.
- `assert_enum_and_str_reps_valid`: Asserts that an Enum member and its string representation(s)
    are valid and not `None` or empty.
- `assert_str_reps_valid`: Asserts that a sequence of string representation(s) does not
    contain duplicates.
- `make_enum_to_strings_dict`: Creates a mapping of enum members to their string representation(s).
- `make_string_to_enum_dict`: Creates a mapping of string representation(s) to their corresponding
    enum members.
- `make_enum_and_str_rep_dicts`: Creates both string-to-enum and enum-to-string representation(s)
    dictionaries for a given Enum class.

Copyright 2025 Daniel Robert Jackson
"""

"""
Standard Libraries
"""
from collections import defaultdict
from collections.abc import Iterable
from enum   import Enum
from typing import Collection, Hashable, Mapping, Optional, Sequence, Union
from typing_extensions import overload, TypeAlias, TypeVar

from ..type_checks import (
    T,
    set_name, set_name_if,
    set_docstring, set_docstring_if,
    set_name_and_doc, set_name_and_doc_if,
)
__all__ = [
    # Assertion Functions
    "assert_enum_and_str_reps_exist",
    "assert_enum_and_str_reps_valid",
    "assert_str_reps_valid",
    "make_enum_to_strings_dict",
    "make_string_to_enum_dict",
    "make_enum_and_str_rep_dicts",
]

T = TypeVar("T", bound=object)
"""Type variable for generic objects."""

Many: TypeAlias = Collection[T]
"""Type variable for collections that can contain many items."""

OneOrMany: TypeAlias = Union[T, Many[T]]
"""Type variable for collections that can contain one or more items."""

ValueOrValues: TypeAlias = OneOrMany[T]
"""Value or collection of values."""

Key = TypeVar("Key", bound=Hashable)
"""Key type variable for dictionaries."""

Keys: TypeAlias = Many[Key]
"""Keys type variable for iterable collections of keys."""

KeyOrKeys: TypeAlias = Union[Key, Keys]
"""Key or keys type variable for collections that can be a single key or an iterable of keys."""

It = TypeVar("It", bound=Iterable[object])
"""Iterable type variable for collections that can be iterated over."""

Col = TypeVar("Col", bound=Collection[object])
"""Collection type variable for iterable collections."""

Map = TypeVar("Map", bound=Mapping[Key, T])
"""Mapping type variable for mappings with keys of type Key and values of type Value."""

def _get_description(
    obj:         object,
    description: Optional[str] = None
    ) -> str:
    """
    Get the description of an object, either from the provided description
    or from the type name of the object.

    Args:
        obj:         The object to describe
        description: Optional description of the object

    Returns:
        The description or type name of the object.
    """
    return description or type(obj).__name__

def maybe_set_name(
    obj:  T,
    name: Optional[str] = None
    ) -> T:
    """
    Set the name of an object if it has a `__name__` attribute.
    This is useful for debugging and logging purposes.

    Args:
        obj:  The object to set the name for
        name: Optional name to set for the object

    Returns:
        The object with the name set, if applicable.
    """
    if hasattr(obj, "__name__") and name is not None:
        obj.__name__ = name
    return obj

def check_has_valids(
    iterable:    Iterable,
    description: Optional[str] = None
    ) -> str:
    """
    Check if the iterable collection is inspectable.
    This is used as a precondition for other collection checks, which is why we return the
    description of the collection.

    Args:
        iterable:    An iterable collection to check
        description: Optional description of the collection for error messages

    Returns:
        The description or type name of the collection.

    Raises:
        ValueError: If the collection is None
        TypeError: If the collection is not an iterable
    """
    description = _get_description(iterable, description)
    if iterable is None:
        raise ValueError(f"The {description} must not be None.")

    if not isinstance(iterable, Iterable):
        raise TypeError(
            f"The {description} must be an iterable collection, not {type(iterable).__name__}."
        )

    return description

def is_empty(
    iterable:    Iterable,
    description: Optional[str] = None
    ) -> bool:
    """
    Check if the iterable collection is empty.

    Args:
        iterable:    An iterable collection to check
        description: Optional description of the collection for error messages

    Returns:
        True if the collection is empty, False otherwise.

    Raises:
        ValueError: If the collection is None
        TypeError: If the collection is not an iterable
    """
    _check_collection_inspectable(iterable, description)
    return len(iterable) == 0

def is_not_empty(
    iterable:    Iterable,
    description: Optional[str] = None
    ) -> bool:
    """
    Check if the iterable collection is not empty.

    Args:
        iterable:    An iterable collection to check
        description: Optional description of the collection for error messages

    Returns:
        True if the collection is not empty, False otherwise.

    Raises:
        ValueError: If the collection is None
        TypeError: If the collection is not an iterable
    """
    _check_collection_inspectable(iterable, description)
    return len(iterable) > 0

def check_empty(
    iterable:    It,
    description: Optional[str] = None
    ) -> It:
    """
    Check that the iterable collection is empty.

    Args:
        iterable:    An iterable collection to check
        description: Optional description of the collection for error messages

    Raises:
        ValueError: If the collection is None or not empty
        TypeError: If the collection is not an iterable
    """
    description = _check_collection_inspectable(iterable, description)
    if len(iterable) > 0:
        raise ValueError(
            f"The {description} must be empty, but it contains {len(iterable)} elements."
        )
    return iterable

def check_not_empty(
    iterable:    It,
    description: Optional[str] = None
    ) -> It:
    """
    Check that the iterable collection is not empty.

    Args:
        iterable:    An iterable collection to check
        description: Optional description of the collection for error messages

    Raises:
        ValueError: If the collection is None or empty
        TypeError: If the collection is not an iterable
    """
    description = _check_collection_inspectable(iterable, description)
    if len(iterable) == 0:
        raise ValueError(f"The {description} must not be empty.")
    return iterable

def get_element_type(
    iterable:    Iterable,
    description: Optional[str] = None
    ) -> type:
    """
    Get the type of the first real element in a collection.

    Args:
        iterable:    An iterable collection to check
        description: Optional description of the collection for error messages

    Returns:
        The type of the first real element in the collection.
        This will be `None` if the collection is empty or contains only `None` elements.

    Raises:
        ValueError: If the collection is None
        TypeError: If the collection is not an iterable
    """
    description = _check_collection_inspectable(iterable, description)

    element_type = None
    while element_type is None:
        try:
            # Attempt to get the first element
            element = next(iter(iterable))
            element_type = type(element) if element is not None else None
        except StopIteration:
            break # Every element must be None, so we will return None

    return element_type

def get_key_type(
    map: Map,
    description: Optional[str] = None
    ) -> type:
    """
    Get the type of the keys in a mapping.

    Args:
        map:         A mapping of keys to values
        description: Optional description of the mapping for error messages

    Returns:
        The type of the keys in the mapping.
        
    Raises:
        ValueError: If the mapping is None
        TypeError: If the mapping is not a valid mapping type
    """
    col_type_name = type(map).__name__
    description = description or col_type_name


    if map is None:
        raise ValueError(f"The {description} must not be None.")
    if not isinstance(map, Mapping):
        raise TypeError(
            f"The {description} must be a mapping, not {col_type_name}."
        )

    key_type = None
    while key_type is None:
        try:
            # Attempt to get the first key
            key = next(iter(map.keys()))
            key_type = type(key) if key is not None else None
        except StopIteration:
            break # Every key must be None, so we will return None

    return key_type

def get_value_type(
    map: Map,
    description: Optional[str] = None
    ) -> type:
    """
    Get the type of the values in a mapping.

    Args:
        map:         A mapping of keys to values
        description: Optional description of the mapping for error messages

    Returns:
        The type of the values in the mapping.

    Raises:
        ValueError: If the mapping is None
        TypeError: If the mapping is not a valid mapping type
    """
    col_type_name = type(map).__name__
    description = description or col_type_name

    if map is None:
        raise ValueError(f"The {description} must not be None.")

def assert_not_empty(
    collection:  Iterable,
    description: Optional[str] = None
    ) -> None:
    """
    Assert that the collection is not empty or None

    Args:
        collection:  An iterable collection to check
        description: Optional description of the sequence for error messages

    Raises:
        AssertionError: If the collection is empty or None
    """
    description = description or type(collection).__name__
    assert collection is not None, f"The {description} must not be None."
    assert len(collection) > 0, f"The {description} must not be empty."

def assert_lengths_match(
    collection1: Iterable,
    collection2: Iterable,
    description1: Optional[str] = None,
    description2: Optional[str] = None
    ) -> None:
    """
    Assert that the lengths of two collections match and that neither is empty.

    Args:
        collection1:  The first iterable collection
        collection2:  The second iterable collection
        description1: Optional description of the first collection for error messages
        description2: Optional description of the second collection for error messages

    Raises:
        AssertionError: If the lengths of the two collections do not match or if either is empty.
    """
    assert_not_empty(collection1, description1)
    assert_not_empty(collection2, description2)

    element_type1 = f"[{type(next(iter(collection1)))!r}]"
    element_type2 = f"[{type(next(iter(collection2)))!r}]"
    len1 = len(collection1)
    len2 = len(collection2)
    description1 = description1 or f"{type(collection1).__name__}{element_type1}"
    description2 = description2 or f"{type(collection2).__name__}{element_type2}"
    assert len1 == len2, \
        f"The lengths of {description1} and {description2} must match: " \
        f"{len1} != {len2}."

def assert_keys(
    map:           Map,
    included_keys: Optional[KeyOrKeys] = None,
    excluded_keys: Optional[KeyOrKeys] = (None,),
    description:   Optional[str]        = None
    ) -> None:
    """
    Check that the mapping:
    -   is not empty or None
    -   contains all included keys (if provided)
    -   does not contain any excluded keys (or just does not contain the `None` key by default).

    Args:
        map:           A mapping of keys to values
        included_keys: Optional iterable of keys that must be present in the mapping
        excluded_keys: Optional iterable of keys that must not be present in the mapping.
            Defaults to a tuple containing `None`, which means that the `None` key is excluded
        description:   Optional description of the mapping for error messages

    Raises:
        AssertionError: If the mapping
            -   is empty or None
            -   does not contain all included keys
            -   contains any excluded keys.
    """
    assert_not_empty(map, description)

    description = description or type(map).__name__
    keys_type   = f" ({type(next(iter(map)))})" if map else ""

    if included_keys is not None:
        if isinstance(included_keys, Key):
            included_keys = (included_keys,)

        for key in included_keys:
            assert key in map, \
                f"The {description} must contain the key{keys_type!r}: {key!r}."

    if excluded_keys is not None:
        if isinstance(excluded_keys, Key):
            excluded_keys = (excluded_keys,)

        for key in excluded_keys:
            assert key not in map, \
                f"The {description} must not contain the key{keys_type!r}: {key!r}."

def assert_values(
    map:             Map,
    included_values: ValueOrValues = None,
    excluded_values: ValueOrValues = (None,),
    description:     Optional[str] = None
    ) -> None:
    """
    Check that the mapping:
    -   is not empty or None
    -   contains all included values (if provided)
    -   does not contain any excluded values (or just does not contain the `None` value by default).
    
    Args:
        map:             A mapping of keys to values
        included_values: Optional iterable of values that must be present in the mapping
        excluded_values: Optional iterable of values that must not be present in the mapping.
            Defaults to a tuple containing `None`, which means that the `None` value is excluded
        description:     Optional description of the mapping for error messages
        
    Raises:
        AssertionError: If the mapping
            -   is empty or None
            -   does not contain all included values
            -   contains any excluded values.
    """
    assert_not_empty(map, description)

    description = description or type(map).__name__
    values_type = f" ({type(next(iter(map.values())))})" if map else ""

    if included_values is not None:
        if isinstance(included_values, Value):
            included_values = (included_values,)

        for value in included_values:
            assert value in map.values(), \
                f"The {description} must contain the value{values_type!r}: {value!r}."

    if excluded_values is not None:
        if isinstance(excluded_values, Value):
            excluded_values = (excluded_values,)

        for value in excluded_values:
            assert value not in map.values(), \
                f"The {description} must not contain the value{values_type!r}: {value!r}."

@overload
def assert_contains(
    map:         Map,
    keys:        KeyOrKeys,
    description: Optional[str] = None
    ) -> None:
    """
    Assert that the mapping contains the specified key.

    Args:
        map:         A mapping of keys to values
        keys:        A single key or an iterable of keys that must be present in the mapping
        description: Optional description of the mapping for error messages

    Raises:
        AssertionError: If the mapping does not contain the specified key(s).
    """
    assert_not_empty(map, description)

    key_type   = None
    value_type = None

    while key_type is None or value_type is None:
        try:
            key_type   = type(next(iter(map.keys())))   if key_type   is None else key_type
            value_type = type(next(iter(map.values()))) if value_type is None else value_type
        except StopIteration:
            # This can only happen if the only key in the map is None, or if every value in the map
            # is None.
            break

    

    description = description or f"{type(map).__name__}[{key_type!r}, {value_type!r}]"