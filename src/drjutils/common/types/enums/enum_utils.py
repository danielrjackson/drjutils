"""
# enum_utils.py

## drjutils.common.enums

## Summary

This module provides utilities for working with enumerations in Python.

## Data Types:
- `EnumType`: A type variable for concrete Enum types.
- `StrReps`: A type alias for a tuple of string representation(s) for an Enum instance.
- `EnumToStrRepsDict`: A type alias for a dictionary mapping Enum members to their respective
    ordered list of string representation(s).
- `StrToEnumDict`: A type alias for a dictionary mapping string representation(s) to their
    corresponding Enum members.

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

## Private Methods:
- `_assert_valid_str_keys`: Checks that the string-to-enum mapping does not contain any empty
    strings or `None`, and that the dictionary is not empty.
- `_assert_valid_enum_keys`: Checks that the enum-to-string representation(s) mapping does not
    contain any `None` Enum members, and that the dictionary is not empty.
- `_assert_enum_exists`: Asserts that the Enum member exists and is not `None` for a given string
    representations.
- `_assert_str_reps_exist`: Asserts that the string representation(s) exist and are not empty or `None`.
- `_assert_not_empty`: Asserts that a collection is not empty.
- `_assert_lengths_match`: Asserts that the lengths of the enums and string representation(s)
    sequences match.
- `_process_enum_set`: Processes a set of enum members and their string representation(s), ensuring
    uniqueness and non-emptiness of strings.

Copyright 2025 Daniel Robert Jackson
"""

"""
Standard Libraries
"""
from collections import defaultdict
from collections.abc import Iterable
from enum   import Enum
from typing import Mapping, Optional, Sequence
from typing_extensions import Overload, TypeAlias, TypeVar

"""
Project Libraries
"""
from drjutils.common.types.sentinel import Opt, UNSET

__all__ = [
    # Data Types
    "EnumType",
    "EnumToStrRepDict",
    "EnumToStrRepsDict",
    "EnumToStrRepOrRepsDict",
    "StrRepToEnumDict",
    "StrReps",
    "StrRepOrReps",
    # Utility Functions
    "assert_enum_and_str_reps_exist",
    "assert_enum_and_str_reps_valid",
    "assert_str_reps_valid",
    "make_enum_to_strings_dict",
    "make_string_to_enum_dict",
    "make_enum_and_str_rep_dicts",
]

EnumType = TypeVar("EnumType", bound=Enum)
"""
Concrete type variable for Enum types.
"""

StrReps: TypeAlias = tuple[str, ...]
"""
StringReps is a type alias for a tuple of string representation(s) for an Enum instance.
"""

StrRepOrReps: TypeAlias = str | StrReps
"""
StrRepOrReps is a type alias for either a tuple of string representation(s) or a single string
representation.
"""

EnumToStrRepDict: TypeAlias = dict[EnumType, str]
"""
EnumToStrRepDict is a type alias for a dictionary mapping Enum members to their corresponding string
representation.
"""

EnumToStrRepsDict: TypeAlias = dict[EnumType, StrReps]
"""
EnumToStrRepsDict is a type alias for a dictionary mapping Enum members to their respecitve ordered
list of string representation(s).
"""

EnumToStrRepOrRepsDict: TypeAlias = dict[EnumType, str] | dict[EnumType, StrReps]
"""
EnumToStrRepOrRepsDict is a type alias for a dictionary mapping Enum members to either a single string
or a tuple of string representation(s).
"""

StrRepToEnumDict: TypeAlias = dict[str, EnumType]
"""
StrRepToEnumDict is a type alias for a dictionary mapping each string representation to their
corresponding Enum member.
"""

_StrReps: TypeAlias = Sequence[str]
"""
_StrReps is a type alias for a sequence of string representation(s) for an Enum instance.
"""

_StrRepOrReps: TypeAlias = str | _StrReps
"""
_StrRepOrReps is a type alias for either a sequence of string representation(s) or a single string
representation.
"""

_EnumToStrRepOrRepsMap: TypeAlias = Mapping[EnumType, str] | Mapping[EnumType, _StrReps]
"""
_EnumToStrRepOrRepsMap is a type alias for a mapping of Enum members to either a single string
representation or a sequence of string representation(s).
"""

_StrRepToEnumMap: TypeAlias = Mapping[str, EnumType]
"""
_StrRepToEnumMap is a type alias for a mapping of each string representation to their corresponding
Enum member.
"""

_K  = TypeVar("_K", bound=object)
"""Key type variable for dictionaries."""

_Ks = TypeVar("_Ks", bound=Iterable[_K])
"""Keys type variable for iterable collections of keys."""

_V  = TypeVar("_V", bound=object)
"""Value type variable for dictionaries."""

_Vs = TypeVar("_Vs", bound=Iterable[_V])
"""Values type variable for iterable collections of values."""

_M  = TypeVar("_M", bound=Mapping[_K, _V])
"""Mapping type variable for mappings with keys of type _K and values of type _V."""

def _assert_enum_exists(
    enum:     EnumType,
    str_reps: Optional[StrRepOrReps] = None
    ) -> None:
    """
    Assert that the Enum member exists and is not None.
    Args:
        enum:     The Enum member to check.
        str_reps: Optional sequence of string representation(s) for the Enum member.
        
    Raises:
        AssertionError: If the Enum member is None.
    """
    assert enum is not None, \
        "The Enum must not be None." if str_reps is None else \
            f"The Enum must not be None. \
            Please provide a valid Enum member with corresponding string representation(s) \
            ({str_reps!r})."

def _assert_keys(
    map:           _M,
    description:   Optional[str] = None,
    *,
    allow_none:    bool = False,
    allow_empty:   bool = False,
    included_keys: _Ks = UNSET,
    excluded_keys: _Ks = UNSET,
    ) -> None:
    """
    Check that the mapping is not empty, and if specified, that it contains the included keys
    and/or does not contain the excluded keys.

    Args:
        map:           A mapping of keys to values.
        description:   Optional description of the mapping for error messages.
        included_keys: An iterable of keys that should be present in the mapping.
        excluded_keys: An iterable of keys that should not be present in the mapping.

    Raises:
        AssertionError: If the mapping is empty or includes/excludes keys that do not match the
            specified conditions.
    """
    description = description or type(map).__name__
    keys_type = type(next(iter(map.keys())))

    assert map is not None, f"The {description} must not be None."

    assert map != {}, f"The {description} must not be empty."

    if included_keys is not UNSET:
        for key in included_keys:
            assert key in map, \
                f"The {description} must contain the key ({keys_type!r}): {key!r}."

    if excluded_keys is not UNSET:
        for key in excluded_keys:
            assert key not in map, \
                f"The {description} must not contain the key ({keys_type!r}): {key!r}."

def _assert_not_empty(
    collection:  Iterable,
    description: Optional[str] = None
    ) -> None:
    """
    Assert that the collection is not empty.

    Args:
        collection:  An iterable collection to check.
        description: Optional description of the sequence for error messages.

    Raises:
        AssertionError: If the collection is empty or None.
    """
    assert collection is not None, \
        f"The collection must not be None." if description is None else \
        f"The {description} must not be None."
    description = description or type(collection).__name__
    assert collection, \
        f"The {description} must not be empty."

def _assert_lengths_match(
    enums:         Sequence[EnumType],
    str_reps_list: Sequence[_StrRepOrReps]
    ) -> None:
    """
    Assert that the lengths of the enums and string representation(s) sequences match.

    Args:
        enums:         A sequence of Enum members.
        str_reps_list: A sequence of string representation(s).

    Raises:
        AssertionError: If the lengths of the enums and string representation(s) sequences do not
            match.
    """
    _assert_not_empty(enums, "enums")
    _assert_not_empty(str_reps_list, "string representation(s)")
    assert len(enums) == len(str_reps_list), \
        f"The length of enums [{len(enums)}] and \
            string representation(s) [{len(str_reps_list)}] \
            must be the same for mapping between enums and strings.\n \
            Enums:   {type(next(iter(enums)))!r}::{enums!r}\n \
            Strings: {str_reps_list!r}"

def _assert_str_reps_exist(
    str_reps: _StrRepOrReps,
    enum:     Optional[EnumType] = None
    ) -> None:
    """
    Assert that the string representation(s) exist and are not empty or None.

    Args:
        str_reps: A sequence of string representation(s) for the Enum member.
        enum: Optional Enum member for logging purposes.

    Raises:
        AssertionError: If any of the following conditions are met:
            *   the sequence of string representation(s) is empty or None
            *   any string representation is empty
    """
    assert str_reps, \
        f"Enum member {enum!r} has no string representation(s)." if enum else \
        "The sequence of string representation(s) for an Enum is empty or None."
    if isinstance(str_reps, Sequence):
        for str_rep in str_reps:
            assert str_rep, \
                f"Empty string found for enum member {enum!r} in string representation(s) \
                    {str_reps!r}." \
                    if enum else \
                f"Empty string found in string representation(s) {str_reps!r}."

def _assert_valid_enum_keys(enum_to_str_reps_map: _EnumToStrRepOrRepsMap[EnumType]) -> None:
    """
    Check that the enum-to-string representation(s) mapping does not contain any `None` Enum members.
    Also check that the mapping is not empty.

    Args:
        enum_to_str_reps_map: A map of Enum members to their string representation(s).

    Raises:
        AssertionError: If any `Enum` member is None, or if the map is empty.
    """
    _assert_keys(enum_to_str_reps_map, description="EnumToStrRepsDict")

def _assert_valid_str_keys(str_rep_to_enum_map: _StrRepToEnumMap[EnumType]) -> None:
    """
    Check that the string-to-enum mapping does not contain any empty strings.
    Also check that the map is not empty.

    Args:
        str_rep_to_enum_map: A map mapping string representation(s) to their corresponding
            Enum members.

    Raises:
        AssertionError: If any string representation is empty or `None`, or if the map is
            empty.
    """
    _assert_keys(str_rep_to_enum_map, excluded_keys=("", None), description="StrRepToEnumDict")

def _assert_enum_and_str_reps_exist(
    enum:     EnumType,
    str_reps: Optional[_StrRepOrReps] = None
    ) -> None:
    """
    Assert that the Enum member and its string representation(s) exist and are not None or empty.
    
    Args:
        enum:     The Enum member to check.
        str_reps: Sequence of (or single) string representation(s) for the Enum member.
        
    Raises:
        AssertionError: If any of the following conditions are met:
            *   the Enum member is None
            *   the sequence of string representation(s) is empty or None
            *   any string representation is empty
    """
    _assert_enum_exists(enum, str_reps)
    _assert_str_reps_exist(str_reps, enum)

def _assert_str_reps_valid(
    str_reps:    _StrRepOrReps,
    enum:        Optional[EnumType] = None,
    description: Optional[str]      = None
    ) -> None:
    """
    Assert that the sequence of string representation(s) does not contain duplicates.
    Args:
        str_reps:    A sequence of string representation(s) for the Enum member.
        enum:        Optional Enum member for logging purposes.
        description: Optional description of the Enum member for error messages.
    Raises:
        AssertionError: If the sequence of string representation(s) is empty or None, or if any
            string representation is empty, or if there are duplicate string representation(s).
    """
    _assert_str_reps_exist(str_reps, enum)

    if isinstance(str_reps, Sequence):
        # Check for empty strings in the sequence
        for str_rep in str_reps:
            assert str_rep, \
                f"Empty string found in string representation(s) {str_reps!r}." \
                    if enum is None and description is None else \
                f"Empty string found in string representation(s) {str_reps!r} for {enum!r}." \
                    if enum is not None and description is None else \
                f"Empty string found in string representation(s) {str_reps!r} for {description}." \
                    if enum is None and description is not None else \
                f"Empty string found in string representation(s) {str_reps!r} for {description} \
                    ({enum!r})."

def _process_enum_set(
    enum:                  EnumType,
    str_reps:              _StrRepOrReps,
    str_rep_to_enum_dict:  StrRepToEnumDict[EnumType],
    enum_to_str_reps_dict: Optional[EnumToStrRepOrRepsDict[EnumType]] = None
    ) -> None:
    """
    Private method to process the next set of enums and their string representation(s).

    This method adds the enum/string representation(s) pairs to str_rep_to_enum_dict.
    This is a helper method for `make_string_to_enum_dict` methods.
    If `enum_to_str_reps_dict` is provided, it will also add the enum to its
    corresponding tuple of string representation(s).

    Args:
        enum:                  The Enum member to be added.
        str_reps:              A sequence of string representation(s) for the Enum member.
        str_rep_to_enum_dict:  A dictionary mapping each string representation to their
            corresponding Enum member.
        enum_to_str_reps_dict: An optional dictionary mapping Enum members to their tuple of string
            representation(s).

    Raises:
        AssertionError: If any of the following conditions are met:
            *   any `Enum` member is None
            *   any `Enum` member has no string representation(s)
            *   any of the strings are empty or None
            *   there are duplicate string representation(s) for different Enum members
            *   the Enum or string representation(s) have already been added to the
                `str_rep_to_enum_dict` or `enum_to_str_reps_dict`.
    """
    _assert_enum_and_str_reps_exist(enum, str_reps)

    for string in str_reps:
        assert string not in str_rep_to_enum_dict, \
            f"Duplicate string '{string}' found for {str_rep_to_enum_dict[string]!r} and {enum!r}."
        str_rep_to_enum_dict[string] = enum

    if enum_to_str_reps_dict is not None:
        assert enum not in enum_to_str_reps_dict, \
            f"Duplicate enum {enum!r} found in enum_to_str_reps_dict."
        enum_to_str_reps_dict[enum] = tuple(str_reps)

assert_enum_and_str_reps_exist = _assert_enum_and_str_reps_exist

def assert_enum_and_str_reps_valid(
    enum:        EnumType,
    str_reps:    _StrRepOrReps,
    description: Optional[str] = None
    ) -> None:
    """
    Assert that the Enum member and its string representation(s) are valid.
    Args:
        enum:        The Enum member to check.
        str_reps:    A sequence of string representation(s) for the Enum member.
        description: Optional description of the Enum member for error messages.
    Raises:
        AssertionError: If any of the following conditions are met:
            *   the Enum member is None
            *   the sequence of string representation(s) is empty or None
            *   any string representation is empty
    """
    _assert_enum_and_str_reps_exist(enum, str_reps)
    _assert_str_reps_valid(str_reps, enum, description)

assert_str_reps_valid = _assert_str_reps_valid

@Overload
def make_enum_to_strings_dict(
    enum_to_str_reps_map:  Mapping[EnumType, Sequence[str]]
    ) -> EnumToStrRepsDict[EnumType]:
    """
    Create a dictionary of Enum members to their tuples of string representation(s).

    Args:
        enum_to_str_reps_map: A mapping of Enum members to their sequences of string
            representations.

    Returns:
        A dictionary of Enum members to their tuples of string representation(s).

    Raises:
        AssertionError: If any of the following conditions are met:
            *   no data is provided to process
            *   any `Enum` member is None
            *   any `Enum` member has no string representation(s)
            *   any of the strings are empty or None
            *   there are duplicate string representation(s) for different Enum members
    """
    _assert_valid_enum_keys(enum_to_str_reps_map)
    enum_to_str_reps_dict: EnumToStrRepsDict[EnumType] = enum_to_str_reps_map
    str_rep_to_enum_dict:  StrRepToEnumDict[EnumType]     = {} # For checking uniqueness

    for enum, strings in enum_to_str_reps_map.items():
        _process_enum_set(enum, strings, str_rep_to_enum_dict, enum_to_str_reps_dict)

    return enum_to_str_reps_dict

@Overload
def make_enum_to_strings_dict(
    enum_to_str_reps_pairs: Sequence[tuple[EnumType, _StrReps]],
    enum_to_str_reps_dict:  Optional[EnumToStrRepOrRepsDict[EnumType]] = {}
    ) -> EnumToStrRepsDict[EnumType]:
    """
    Create a mapping of `Enum` members to their string representation(s).

    Args:
        enum_to_str_reps_pairs: `tuple`s, where each `tuple` contains an `Enum` member and
            string representation(s) for that `Enum` member.
        enum_to_str_reps_dict: An optional dictionary mapping `Enum` members to their `tuple` of
            string representation(s). If provided, it will be updated with the new mappings.

    Returns:
        A dictionary mapping `Enum` members to their tuple of string representation(s).
        If `enum_to_str_reps_dict` is provided, it will be updated with the new mappings and
        returned.

    Raises:
        AssertionError: If any of the following conditions are met:
            *   no data is provided to process
            *   any `Enum` member is None
            *   any `Enum` member has no string representation(s)
            *   any of the strings are empty or None
            *   there are duplicate string representation(s) for different Enum members
            *   `enum_to_str_reps_dict` already contains any of the values in
                `enum_to_str_reps_pairs`
    """
    _assert_not_empty(enum_to_str_reps_pairs, "enum_to_str_reps_pairs")
    str_rep_to_enum_dict: StrRepToEnumDict[EnumType] = {}  # For checking uniqueness

    for enum, strings in enum_to_str_reps_pairs:
        _process_enum_set(enum, strings, str_rep_to_enum_dict, enum_to_str_reps_dict)

    return enum_to_str_reps_dict

@Overload
def make_enum_to_strings_dict(
    enums:                 Sequence[EnumType],
    str_reps_list:         Sequence[Sequence[str]],
    enum_to_str_reps_dict: Optional[EnumToStrRepsDict[EnumType]] = {},
) -> EnumToStrRepsDict[EnumType]:
    """
    Create a mapping of Enum members to their string representation(s).

    Args:
        enums:         A sequence of Enum members.
        str_reps_list: A sequence of string representation(s), where each element string
            representation(s) for the corresponding Enum member.

    Returns:
        A dictionary mapping Enum members to their tuple of string representation(s).
        If `enum_to_str_reps_dict` is provided, it will be updated with the new mappings and
        returned.

    Raises:
        AssertionError: If any of the following conditions are met:
            *   no data is provided to process
            *   any `Enum` member is None
            *   any `Enum` member has no string representation(s)
            *   any of the strings are empty or None
            *   there are duplicate string representation(s) for different Enum members
            *   the lengths of the enums and strings sequences do not match
            *   `enum_to_str_reps_dict` already contains any of the values in `enums` or
                `str_reps_list`
    """
    _assert_lengths_match(enums, str_reps_list)

    str_rep_to_enum_dict: StrRepToEnumDict[EnumType] = {} # For checking uniqueness

    for i in range(len(enums)):
        _process_enum_set(enums[i], str_reps_list[i], str_rep_to_enum_dict, enum_to_str_reps_dict)

    return enum_to_str_reps_dict

@Overload
def make_enum_to_strings_dict(
    str_rep_to_enum_dict:  StrRepToEnumDict,
    enum_to_str_reps_dict: Optional[EnumToStrRepsDict[EnumType]] = {}
) -> EnumToStrRepsDict[EnumType]:
    """
    Create a mapping of Enum members to their string representation(s) from a string-to-enum
    mapping.

    Args:
        str_rep_to_enum_dict:  A dictionary mapping each string representation to their
            corresponding Enum member.
        enum_to_str_reps_dict: An optional dictionary mapping Enum members to their tuple of
            string representation(s). If provided, it will be updated with the new mappings.

    Returns:
        A dictionary mapping Enum members to their tuple of string representation(s).
        If `enum_to_str_reps_dict` is provided, it will be updated with the new mappings and
        returned.

    Raises:
        AssertionError: If any of the following conditions are met:
            *   no data is provided to process
            *   any `Enum` member is None
            *   any of the strings are empty or None
    """
    _assert_valid_str_keys(str_rep_to_enum_dict)

    enum_to_str_reps: defaultdict[Enum, list[str]] = defaultdict(list)

    for enum, str_reps in enum_to_str_reps_dict.items():
        enum_to_str_reps[enum] = list(str_reps)

    for str_rep, enum in str_rep_to_enum_dict.items():
        assert_enum_and_str_reps_exist(enum, [str_rep])
        enum_to_str_reps[enum].append(str_rep)

    # Add the new mappings to the enum_to_str_reps_dict
    for enum, strings in enum_to_str_reps.items():
        assert_enum_and_str_reps_valid(enum, strings, "enum_to_str_reps_dict")
        enum_to_str_reps_dict[enum] = tuple(strings)

    return enum_to_str_reps_dict

@Overload
def make_string_to_enum_dict(
    enum_to_str_reps_map: Mapping[EnumType, Sequence[str]],
    str_rep_to_enum_dict: Optional[StrRepToEnumDict[EnumType]] = {}
    ) -> StrRepToEnumDict[EnumType]:
    """
    Create a mapping of string representation(s) to their corresponding Enum members.

    Args:
        enum_to_str_reps_map: A dictionary mapping Enum members to sequences of strings.
        str_rep_to_enum_dict: An optional dictionary mapping each string representation to their
            corresponding Enum member. If provided, it will be updated with the new mappings.

    Returns:
        A dictionary mapping string representation(s) to their corresponding Enum members.
        If `str_rep_to_enum_dict` is provided, it will be updated with the new mappings and
        returned.

    Raises:
        AssertionError: If any of the following conditions are met:
            *   no data is provided to process
            *   any `Enum` member is None
            *   any `Enum` member has no string representation(s)
            *   any of the strings are empty or None
            *   there are duplicate string representation(s) for different Enum members
    """
    _assert_valid_enum_keys(enum_to_str_reps_map)
    for enum, strings in enum_to_str_reps_map.items():
        _process_enum_set(enum, strings, str_rep_to_enum_dict)
    return str_rep_to_enum_dict

@Overload
def make_string_to_enum_dict(
    enum_to_str_reps_pairs: Sequence[tuple[Enum, Sequence[str]]],
    str_rep_to_enum_dict:   Optional[StrRepToEnumDict[EnumType]] = {}
    ) -> StrRepToEnumDict[EnumType]:
    """
    Create a mapping of string representation(s) to their corresponding Enum members.

    Args:
        enum_to_str_reps_pairs: A sequence of tuples, where each tuple contains an Enum member and a
            sequence of strings.
        str_rep_to_enum_dict:   An optional dictionary mapping each string representation to their
            corresponding Enum member. If provided, it will be updated with the new mappings.

    Returns:
        A dictionary mapping string representation(s) to their corresponding Enum members.
        If `str_rep_to_enum_dict` is provided, it will be updated with the new mappings and
        returned.

    Raises:
        AssertionError: If any of the following conditions are met:
            *   no data is provided to process
            *   any `Enum` member is None
            *   any `Enum` member has no string representation(s)
            *   any of the strings are empty or None
            *   there are duplicate string representation(s) for different Enum members
    """
    _assert_not_empty(enum_to_str_reps_pairs, "enum_to_str_reps_pairs")
    for enum, strings in enum_to_str_reps_pairs:
        _process_enum_set(enum, strings, str_rep_to_enum_dict)
    return str_rep_to_enum_dict

@Overload
def make_string_to_enum_dict(
    enums:                Sequence[Enum],
    str_reps_list:        Sequence[Union[Sequence[str], str]],
    str_rep_to_enum_dict: Optional[StrRepToEnumDict[EnumType]] = {}
) -> StrRepToEnumDict[EnumType]:
    """
    Create a mapping of string representation(s) to their corresponding Enum members.

    This method ensures that:
    *   each Enum member has at least one string representation
    *   none of the strings are empty
    *   all string representation(s) are unique
    *   the lengths of the enums and strings sequences match

    Args:
        enums:                A sequence of Enum members.
        str_reps_list:        A sequence of (sequences of strings, or just a string), where each
            element corresponds to an Enum member.
        str_rep_to_enum_dict: An optional dictionary mapping each string representation to their
            corresponding Enum member. If provided, it will be updated with the new mappings.

    Returns:
        A dictionary mapping string representation(s) to their corresponding Enum members.
        If `str_rep_to_enum_dict` is provided, it will be updated with the new mappings and
        returned.

    Raises:
        AssertionError: If any of the following conditions are met:
            *   no data is provided to process
            *   any `Enum` member is None
            *   any `Enum` member has no string representation(s)
            *   any of the strings are empty or None
            *   there are duplicate string representation(s) for different Enum members
    """
    _assert_lengths_match(enums, str_reps_list)
    for i in range(len(enums)):
        _process_enum_set(enums[i], str_reps_list[i], str_rep_to_enum_dict)
    return str_rep_to_enum_dict

def make_enum_and_str_rep_dicts(
    enum_class: EnumType,
    
) -> tuple[EnumToStrRepsDict[EnumType], StrRepToEnumDict[EnumType]]:
    """
    Create both string-to-enum and enum-to-string representation(s) dictionaries.

    Args:
        enum_class: The Enum class to create the mappings for.

    Returns:
        A tuple containing:
        -   A dictionary mapping string representation(s) to their corresponding Enum members.
        -   A dictionary mapping Enum members to their tuple of string representation(s).

    Raises:
        AssertionError: If the Enum class is not valid or does not have string representation(s).
    """
    enum_to_str_reps_dict: EnumToStrRepsDict[EnumType] = {}
    str_rep_to_enum_dict:  StrRepToEnumDict[EnumType]  = {}

    for enum in enum_class:
        if isinstance(enum.value, Sequence) and isinstance(next(iter(enum.value), None), str):
            str_reps = enum.value
        elif isinstance(enum.value, str):
            str_reps = (enum.name,)
        else:
            raise AssertionError(
                f"Enum {enum!r} has an invalid value type: {type(enum.value)!r}. "
                "Expected a sequence of strings or a single string."
            )

        _assert_str_reps_exist(str_reps, enum)
        _process_enum_set(
            enum,
            str_reps,
            str_rep_to_enum_dict,
            enum_to_str_reps_dict)

    return enum_to_str_reps_dict, str_rep_to_enum_dict

def make_enum_and_str_rep_dicts(
    enum_class: EnumType
) -> tuple[EnumToStrRepsDict[EnumType], StrRepToEnumDict[EnumType]]:
    """
    Create both string-to-enum and enum-to-string representation(s) dictionaries.

    Args:
        enum_class: The Enum class to create the mappings for.

    Returns:
        A tuple containing:
        -   A dictionary mapping string representation(s) to their corresponding Enum members.
        -   A dictionary mapping Enum members to their tuple of string representation(s).

    Raises:
        AssertionError: If the Enum class is not valid or does not have string representation(s).
    """
