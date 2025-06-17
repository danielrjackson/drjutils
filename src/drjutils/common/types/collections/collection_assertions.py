"""
# collection_assertions.py

## drjutils.common.enums

## Summary

This module provides utilities for working with enumerations in Python.

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
from typing import Mapping, Optional, Sequence, Union
from typing_extensions import Overload, TypeAlias, TypeVar

__all__ = [
    # Assertion Functions
    "assert_enum_and_str_reps_exist",
    "assert_enum_and_str_reps_valid",
    "assert_str_reps_valid",
    "make_enum_to_strings_dict",
    "make_string_to_enum_dict",
    "make_enum_and_str_rep_dicts",
]

_Key  = TypeVar("_Key", bound=object)
"""Key type variable for dictionaries."""

_Keys = TypeVar("_Keys", bound=Iterable[_Key])
"""Keys type variable for iterable collections of keys."""

_KeyOrKeys = Union[_Key, _Keys]
"""Key or keys type variable for collections that can be a single key or an iterable of keys."""

_Value  = TypeVar("_Value", bound=object)
"""Value type variable for dictionaries."""

_Values = TypeVar("_Values", bound=Iterable[_Value])
"""Values type variable for iterable collections of values."""

_ValueOrValues = Union[_Value, _Values]
"""
Value or values type variable for collections that can be a single value or an iterable of values.
"""

_Map  = TypeVar("_M", bound=Mapping[_Key, _Value])
"""Mapping type variable for mappings with keys of type _Key and values of type _Value."""

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
    map:           _Map,
    included_keys: Optional[_KeyOrKeys] = None,
    excluded_keys: Optional[_KeyOrKeys] = (None,),
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
        if isinstance(included_keys, _Key):
            included_keys = (included_keys,)

        for key in included_keys:
            assert key in map, \
                f"The {description} must contain the key{keys_type!r}: {key!r}."

    if excluded_keys is not None:
        if isinstance(excluded_keys, _Key):
            excluded_keys = (excluded_keys,)

        for key in excluded_keys:
            assert key not in map, \
                f"The {description} must not contain the key{keys_type!r}: {key!r}."

def assert_values(
    map:             _Map,
    included_values: _ValueOrValues = None,
    excluded_values: _ValueOrValues = (None,),
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
        if isinstance(included_values, _Value):
            included_values = (included_values,)

        for value in included_values:
            assert value in map.values(), \
                f"The {description} must contain the value{values_type!r}: {value!r}."

    if excluded_values is not None:
        if isinstance(excluded_values, _Value):
            excluded_values = (excluded_values,)

        for value in excluded_values:
            assert value not in map.values(), \
                f"The {description} must not contain the value{values_type!r}: {value!r}."

@Overload
def assert_contains(
    map:         _Map,
    keys:        _KeyOrKeys,
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