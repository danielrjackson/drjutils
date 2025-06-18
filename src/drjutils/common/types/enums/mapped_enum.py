"""
# enum_map.py

## drjutils.common.enums

## Summary

This module defines a base class for creating enums with string aliases.

## Class: MappedEnum

This class is a base class for mapping enum members to string representations.
It is intended for the use case where there are a relatively small number of string variations
per enum member, and it provides methods for checking and converting strings to enum members.

If a much broader set of string variations is needed, consider using `EnumRegex` instead.

### Example Usage

```python
from typing import Final, Tuple
from drjutils.common.enums import MappedEnum

class MyMappedEnum(MappedEnum):
    BMP:  Final[Tuple[str, ...]] = ("BMP",  "bmp", "Bitmap")
    PNG:  Final[Tuple[str, ...]] = ("PNG",  "png")
    JPEG: Final[Tuple[str, ...]] = ("JPEG", "jpeg")
    GIF:  Final[Tuple[str, ...]] = ("GIF",  "gif")    
```

Copyright 2025 Daniel Robert Jackson
"""

# TODO: Clean up imports once this module is done.

"""
Standard Libraries
"""
from enum   import Enum
from typing import  Optional, Self

"""
Project Libraries
"""
from .enum_utils import (
    EnumType,
    EnumToStrRepsDict,
    StrReps,
    StrRepOrReps,
    StrRepToEnumDict,
    assert_enum_and_str_reps_exist,
    assert_enum_and_str_reps_valid,
    assert_str_reps_valid,
    make_enum_to_strings_dict,
    make_string_to_enum_dict,
    make_enum_and_str_rep_dicts,
)
from drjutils.common.types.sentinel import UNSET

__all__ = [
    "MappedEnum"
]

class MappedEnum(Enum):
    """
    # Class: MappedEnum

    This class is a base class for mapping enum members to string representations.
    It is intended for the use case where there are a relatively small number of string variations
    per enum member, and it provides methods for checking and converting strings to enum members.

    The strings should be in order of preference, meaning that the first string in the tuple
    is the most preferred representation of the enum member, and subsequent strings are
    alternative representations. This allows for a clear and consistent way to map enum members
    to their string representations.

    The first string in the tuple is used as the display string for the enum member,
    which is returned when the enum member is converted to a string. This is useful for
    displaying the enum member in a user-friendly way.

    If a much broader set of string variations is needed, consider using `EnumRegex` instead.

    Warning: Strings should never be duplicated.

    ### Example Usage

    ```python
    from typing import Final, Tuple
    from drjutils.common import MappedEnum

    class MyMappedEnum(MappedEnum):
        BMP:  Final[Tuple[str, ...]] = ("BMP",  "bmp", "Bitmap")
        PNG:  Final[Tuple[str, ...]] = ("PNG",  "png")
        JPEG: Final[Tuple[str, ...]] = ("JPEG", "jpeg")
        GIF:  Final[Tuple[str, ...]] = ("GIF",  "gif")    
    ```
    """

    _ENUMS_TO_STRINGS: EnumToStrRepsDict[Self]
    """
    ### Mapping of all Enum members to their string representations

    *Enums and strings ordered by preference*
    """

    _STRINGS_TO_ENUMS: StrRepToEnumDict[Self]
    """Mapping of all string representations to their corresponding Enum members."""

    def __new__(cls, *value: str) -> Self:
        """
        Create a new instance of the enum with the given string representations.

        This method is called when a new enum member is created. It initializes the
        enum member with the provided string representations and sets the value.

        Args:
            value: A tuple of strings representing the enum member.

        Returns:
            An instance of the enum with the given string representations.

        Raises:
            ValueError: If the value is empty or does not contain valid strings.
        """
        reps = value
        assert_str_reps_valid(reps, Self)

        obj = object.__new__(cls)

        obj._value_ = tuple(reps)
        obj._str_reps = obj._value_
        obj._display_ = obj._value_[0]

        return obj

    def __str__(self) -> str:
        """
        Return the string representation of the enum member.

        This method is called when the enum member is converted to a string.

        Returns:
            The display string of the enum member as defined in the subclass.
        """
        return self._display_

    def get_str_reps(self) -> StrReps:
        """
        Get the string representations of the enum member.

        This method returns the tuple of strings that represent the enum member.

        Returns:
            A tuple of strings representing the enum member.
        """
        return self._str_reps

    @classmethod
    def __init_subclass__(cls) -> None:
        """
        This method is called when a subclass of BooleanAlias is created.

        It ensures that the subclass has defined the required class variables
        and initializes the sets for fast lookup of True and False values.
        It also builds a combined mapping of all valid string values to their
        corresponding boolean values.

        Args:
            cls: The subclass that is being initialized.

        Raises:
            ValueError: If multiple True or False members are found in the subclass.
            AssertionError: If the subclass does not define the required class variables.
        """
        super().__init_subclass__()

        cls._ENUMS_TO_STRINGS, cls._STRINGS_TO_ENUMS = make_enum_and_str_rep_dicts(cls)

    @classmethod
    def is_valid_str(cls, string: str, self = None) -> bool:
        """
        Check if the given string is a valid representation of an enum member.
        This method checks if the provided string matches any of the string representations
        defined for the enum member.

        Args:
            string: The string to check.
            self:   Optional; if provided, checks against the string representations of this
                    specific enum member.

        Returns:
            bool: True if the string is a valid representation of an enum member, False otherwise.
        """
        if self is None:
            return string in cls._STRINGS_TO_ENUMS
        return string in cls._ENUMS_TO_STRINGS[self]

    @classmethod
    def maybe_from_str(cls, string: str) -> Optional[Self]:
        """
        Attempts to convert a string to a BooleanAlias instance if it matches known boolean representations.

        Args:
            string (str): The input string to interpret as a boolean value.

        Returns:
            Optional[BooleanAlias]: Returns BooleanAlias.TRUE or BooleanAlias.FALSE if the string matches a known boolean alias,
            otherwise returns None.
        """
        return cls._STRINGS_TO_ENUMS.get(string)

    @classmethod
    def from_str(cls, string: str) -> Self:
        """
        Converts a string to a BooleanAlias instance.

        Attempts to interpret the given string as a boolean value. If the string cannot be
        interpreted as a boolean, raises a ValueError.

        Args:
            string (str): The string to convert to a BooleanAlias instance.

        Returns:
            BooleanAlias: The BooleanAlias instance corresponding to the input string.

        Raises:
            ValueError: If the input string cannot be interpreted as a boolean.
        """
        result = cls.maybe_from_str(string)
        if result is None:
            raise ValueError(f"Invalid value: {string}")
        return result

