"""
# drjutils.common.enums

# Enums Library

This module provides utilities for working with enumerations in Python.

## Classes

- `MappedEnum`: A class for mapping enum values to their names and vice versa.

## Data Types
- `EnumType`:          Type variable for any enum type.
- `StrReps`:           Type alias for a tuple of string representations of an enum.
- `EnumToStrRepsDict`: Type alias for a dictionary mapping enum values to their string
    representations.
- `StrToEnumDict`:     Type alias for a dictionary mapping strings to their corresponding enum
    values.

## Utility Functions
- `assert_enum_and_str_reps_exist`: Validates that the enum and its string representations exist.
- `assert_enum_and_str_reps_valid`: Validates that the enum and its string representations are
    valid.
- `assert_str_reps_valid`: Validates that the provided string representations are valid for the
    enum.
- `make_enum_to_strings_dict`: Creates a mapping from enum values to their string representations.
- `make_string_to_enum_dict`:  Creates a mapping from strings to their corresponding enum values.
- `make_enum_and_str_rep_dicts`: Creates both enum-to-string and string-to-enum mappings.

Copyright 2025 Daniel Robert Jackson
"""

from .enum_utils import (
    EnumType,
    StrReps,
    EnumToStrRepsDict,
    StrRepToEnumDict,
    assert_enum_and_str_reps_exist,
    assert_enum_and_str_reps_valid,
    assert_str_reps_valid,
    make_enum_to_strings_dict,
    make_string_to_enum_dict,
    make_enum_and_str_rep_dicts,
    )
from .mapped_enum  import MappedEnum
from .enum_regex  import EnumRegex


__all__ = [
    # Classes
    "MappedEnum",
    "EnumRegex",
    # Data Types
    "EnumType",
    "StrReps",
    "EnumToStrRepsDict",
    "StrRepToEnumDict",
    # Utility Functions
    "assert_enum_and_str_reps_exist",
    "assert_enum_and_str_reps_valid",
    "assert_str_reps_valid",
    "make_enum_to_strings_dict",
    "make_string_to_enum_dict",
    "make_enum_and_str_rep_dicts"
]

