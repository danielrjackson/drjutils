"""
# enum_map.py

## drjutils.common.enums

## Summary

This module defines a base class for creating enums with string aliases.

## Class: EnumMap

This class is a base class for mapping enum members to string representations.
It is intended for the use case where there are a relatively small number of string variations
per enum member, and it provides methods for checking and converting strings to enum members.

If a much broader set of string variations is needed, consider using `EnumRegex` instead.

### Example Usage

```python
from typing import Final, Tuple
from drjutils.common.enums import EnumMap

class MyEnumMap(EnumMap):
    BMP:  Final[Tuple[str, ...]] = ("BMP",  "bmp", "Bitmap")
    PNG:  Final[Tuple[str, ...]] = ("PNG",  "png")
    JPEG: Final[Tuple[str, ...]] = ("JPEG", "jpeg")
    GIF:  Final[Tuple[str, ...]] = ("GIF",  "gif")    
```

Copyright 2025 Daniel Robert Jackson
"""

"""
Standard Libraries
"""
from enum   import Enum
from typing import  Optional, Self, Union

"""
Project Libraries
"""
from .enum_utils import (
    EnumType,
    StrReps,
    EnumToStrRepsDict,
    StrToEnumDict,
    assert_enum_and_str_reps_exist,
    assert_enum_and_str_reps_valid,
    assert_str_reps_valid,
    make_enum_to_strings_dict,
    make_string_to_enum_dict,
    make_enum_and_str_rep_dicts,
)

__all__ = [
    "EnumMap"
]

class EnumMap(Enum):
    """
    # Class: EnumMap

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
    from drjutils.common import EnumMap

    class MyEnumMap(EnumMap):
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

    _STRINGS_TO_ENUMS: StrToEnumDict[Self]
    """Mapping of all string representations to their corresponding Enum members."""

    def __new__(cls, value: Union[StrReps, str]) -> Self:
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
        assert_str_reps_valid(value, Self)

        obj = object.__new__(cls)
        obj._value_ = value

        # Use the subclass-specific display string.
        obj._display_ = value[0]

        return obj

    def __str__(self) -> str:
        """
        Return the string representation of the enum member.

        This method is called when the enum member is converted to a string.

        Returns:
            The display string of the enum member as defined in the subclass.
        """
        return self._display_

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
    def is_valid(cls, string: str) -> bool:
        """
        Check if the given string is a valid representation of either True or False.
        This method checks if the string is in the combined mapping of True and False values
        defined in the subclass. It ignores leading and trailing whitespace.
        It is case-sensitive.

        Args:
            string: The string to check.

        Returns:
            bool: True if the string is a valid representation of either True or False, False otherwise.
        """
        return string.strip() in cls._ALL_BOOL_MAP

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
        if cls.is_true(string):
            return cls._get_true_member()
        elif cls.is_false(string):
            return cls._get_false_member()
        else:
            return None

    @classmethod
    def maybe_bool_from_str(cls, string: str) -> Optional[bool]:
        """
        Attempts to convert a string to a boolean value based on predefined mappings.

        Args:
            string (str): The input string to convert.

        Returns:
            Optional[bool]: The corresponding boolean value if the string matches a known alias,
            otherwise None.
        """
        bool_enum = cls.maybe_from_str(string)
        return bool_enum.value if bool_enum is not None else None

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
            raise ValueError(f"Invalid Boolean value: {string}")
        return result

    @classmethod
    def bool_from_str(cls, string: str) -> bool:
        """
        Converts a string to a boolean value.

        Attempts to interpret the given string as a boolean. If the string cannot be
        interpreted as a boolean, raises a ValueError.

        Args:
            string (str): The string to convert to a boolean.

        Returns:
            bool: The boolean value corresponding to the input string.

        Raises:
            ValueError: If the input string cannot be interpreted as a boolean.
        """
        result = cls.maybe_bool_from_str(string)
        if result is None:
            raise ValueError(f"Invalid Boolean value: {string}")
        return result

    @classmethod
    def _get_true_member(cls) -> Self:
        """
        Returns the enum member whose value is True.

        Iterates over all members of the class and returns the first member with a value of True.

        Returns:
            Self: The enum member with value True.

        Raises:
            NotImplementedError: If no member with value True is defined in the subclass.
        """
        for member in cls:
            if member.value is True:
                return member
        raise NotImplementedError("True member not defined in subclass")

    @classmethod
    def _get_false_member(cls) -> Self:
        """
        Returns the enum member whose value is False.

        Iterates through the members of the class and returns the first member
        with a value of False. Raises a ValueError if no such member is found.

        Returns:
            BooleanAlias: The enum member with value False.

        Raises:
            ValueError: If no member with value False is defined in the subclass.
        """
        for member in cls:
            if member.value is False:
                return member
        raise ValueError("False member not defined in subclass")
