"""
# boolean_alias.py

## drjutils.common.bools.boolean_alias

### Summary

This module defines a base class for boolean-like enums with string aliases.
It provides methods for checking, converting, and retrieving boolean values
based on string representations.

This module is part of the drjutils library, which provides common utility
functions for string formatting and parsing.

## Class: BooleanAlias

This class is a base class for creating boolean-like enums with string aliases.
It allows subclasses to define their own string representations for True and False
values, and provides methods for checking and converting strings to boolean values.
It also provides methods for retrieving the corresponding enum member based on
string representations.

### Required Subclass Variables

Subclasses must define the following class variables:

| Class Variable |       Type      |            Description            |
|---------------:|:---------------:|:----------------------------------|
|   `_TRUE_STR` |      `str`      | Display text for True alias.      |
|  `_FALSE_STR` |      `str`      | Display text for False alias.     |
|  `_TRUE_STRINGS` | `Iterable[str]` | Allowed strings for True values.  |
| `_FALSE_STRINGS` | `Iterable[str]` | Allowed strings for False values. |

>    Prefer `Final` for the class variables to ensure they are not modified.

### Example Usage

```python
from typing import Final, Tuple
from drjutils.common.bools import BooleanAlias

class MyYesNo(BooleanAlias):
    # Enum values for True and False.
    YES = True
    NO  = False

    # Display strings for True and False.
    _TRUE_STR:   Final[str]        = "Yes"
    _FALSE_STR:  Final[str]        = "No"
    _TRUE_STRINGS:  Final[Tuple[str]] = ["y", "Y", "yes", "Yes", "YES"]
    _FALSE_STRINGS: Final[Tuple[str]] = ["n", "N", "no", "No", "NO"]
```

Copyright 2025 Daniel Robert Jackson
"""

"""
Standard Libraries
"""
from enum   import Enum
from typing import Dict, Optional, Self, Tuple, Union

class BooleanAlias(Enum):
    """
    # Class: BooleanAlias

    This class is a base class for creating boolean-like enums with string aliases.
    It allows subclasses to define their own string representations for True and False
    values, and provides methods for checking and converting strings to boolean values.
    It also provides methods for retrieving the corresponding enum member based on
    string representations.

    ## Required Subclass Variables

    Subclasses must define the following class variables:

    | Class Variable |       Type      |            Description            |
    |---------------:|:---------------:|:----------------------------------|
    |   `_TRUE_STR` |      `str`      | Display text for True alias.      |
    |  `_FALSE_STR` |      `str`      | Display text for False alias.     |
    |  `_TRUE_STRINGS` | `Iterable[str]` | Allowed strings for True values.  |
    | `_FALSE_STRINGS` | `Iterable[str]` | Allowed strings for False values. |

    >    Prefer `Final` for the class variables to ensure they are not modified.

    ## Boolean Enum Pair with Single String Alias
    
    ```python
    from typing import Tuple
    from drjutils.common.bools import BooleanAlias

    class MyYesNo1(BooleanAlias):
        # Enum values for True and False.
        YES: Tuple[bool, str] = True,  "Yes"
        NO:  Tuple[bool, str] = False, "No"
    ```

    ## Boolean Enum Pair with multiple string aliases

    ```python
    from typing import Tuple
    from drjutils.common.bools import BooleanAlias

    class MyYesNo2(BooleanAlias):
        # Enum values for True and False.
        # This is to properly initialize the enum.
        # The values for the enums will be replaced with just the boolean values.
        # This makes it much more convenient to use them.
        YES: Tuple[bool, Tuple[str]] = True,  ["Yes", "yes", "YES", "y", "Y"]
        NO:  Tuple[bool, Tuple[str]] = False, ["No",  "no",  "NO",  "n", "N"]
    ```

    ## Example Usage with Multiple True/False Pairs

    ```python
    from typing import Tuple
    from drjutils.common.bools import BooleanAlias

    class MyEnabledDisabled(BooleanAlias):
        # Enum values for True and False.
        # This is to properly initialize the enum.
        # The values for the enums will be replaced with just the boolean values.
        # This makes it much more convenient to use them.
        # Make sure that you define them in the order you want them to be paired.
        # The first entry should be the primary True/False enum pair.
        ENABLED:  Tuple[bool, Tuple[str]] = True,  ["Enabled",  "enabled",  "ENABLED"]
        DISABLED: Tuple[bool, Tuple[str]] = False, ["Disabled", "disabled", "DISABLED"]
        ENABLE:   Tuple[bool, Tuple[str]] = True,  ["Enable",   "enable",   "ENABLE"]
        DISABLE:  Tuple[bool, Tuple[str]] = False, ["Disable",  "disable",  "DISABLE"]
    ```
    """

    _ENUM_PAIRS: Dict[Self, Self]
    """Mapping of True to False Enum pairs."""

    _ENUMS_TO_STRINGS: Dict[Self, Tuple[str, ...]]
    """Mapping of Enum members to their string representations (ordered by preference)."""

    _ENUMS_TO_BOOL: Dict[Self, bool]
    """Mapping of Enum members to their boolean values."""

    _TRUE_ENUMS: Tuple[Self, ...]
    """Tuple of all True Enum members."""

    _FALSE_ENUMS: Tuple[Self, ...]
    """Tuple of all False Enum members."""

    @classmethod
    def _make_enum_to_str_mapping(
        mapping: Dict[Self, Tuple[str, ...]]
        ) -> Dict[Self, Tuple[str, ...]]:
        """
        Create a mapping of Enum members to their string representations.
        This method ensures that each Enum member has at least one string representation.

        Args:
            mapping: A dictionary mapping Enum members to their string representations.

        Returns:
            A dictionary mapping Enum members to their string representations.

        Raises:
            ValueError: If any Enum member has no string representations.
        """
        if not isinstance(mapping, dict):
            raise TypeError("Mapping must be a dictionary")
        for enum, string in mapping.items():
            if len(string) == 0:
                raise ValueError(f"{enum!r} needs at least one display string")
        return mapping

    def __new__(cls, value: bool)-> Self:
        """
        Create a new instance of the enum with the given boolean value.
        The display string is set based on the value.
        This method is called when the enum is created.

        Args:
            value: The boolean value (True or False) for the enum member.

        Returns:
            An instance of the enum with the specified boolean value.
        """
        obj         = object.__new__(cls)
        obj._value_ = value

        # Use the subclass-specific display string.
        obj._display_ = cls._TRUE_STRINGS[0] if value else cls._FALSE_STRINGS[0]

        return obj

    def __bool__(self) -> bool:
        """
        Return the boolean value of the enum member.

        This method is called when the enum member is used in a boolean context.
        For example, in an if statement or when converting to a boolean.
        
        Returns:
            The boolean value of the enum member (True or False).
        """
        return self.value

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

        # Initialize this class for the True/False enum pairs.
        # They will be ordereded by the order they are defined in the subclass.
        # Each True/False member must have a matching string(s) member.
        # These primary members won't have underscores around them; that's how we can
        # differentiate them from the string members.
        # The naming convention for the strings members is: `_{BOOL_MEMBER_NAME}_STRINGS`
        # Throw if these aren't present or if every member True member does not have a matching
        # False member that it is paired with.

        # Map of True to False Enum pairs.
        cls._BOOL_PAIRS: Dict[Self, Self] = {}
        """Mapping of True to False Enum pairs."""

        

        true_enum: Optional[Self] = None
        """The current True enum member being processed."""

        false_enum: Optional[Self] = None
        """The current False enum member being processed."""

        for member in cls:
            if true_enum is None:
                # If we don't have a True member yet, we expect one next.
                if member.value is True:
                    true_enum = member
                else:
                    raise AttributeError(
                        f"Expected a True member, but found {member.name}::{member.value}."
                    )
            elif false_enum is None:
                # If we have a True member, we expect a False member next.
                if member.value is False:
                    false_enum = member
                    # Add the pair to the mapping.
                    cls._BOOL_PAIRS[true_enum] = false_enum
                    # Reset for the next pair.
                    true_enum = None
                    false_enum = None
                else:
                    raise AttributeError(
                        f"Expected a False member, but found {member.name}::{member.value}."
                    )

        # If we have a True member but no False member, raise an error.
        if true_enum is not None and false_enum is None:
            raise AttributeError(
                f"Expected a False member after True member {true_enum.name}::{true_enum.value}, \
                    but found none."
            )

        if (
               hasattr(cls, "_PRIM_TRUE_ENUM")
            or hasattr(cls, "_ALT_TRUE_ENUMS")
            or hasattr(cls, "_PRIM_FALSE_ENUM")
            or hasattr(cls, "_ALT_FALSE_ENUMS")
        ):
            # if any of the alternate options are defined,
            # then all of them must be defined.

            # Build an error message if any of the required attributes are missing.
            missing_attributes = []
            if not hasattr(cls, "_PRIM_TRUE_ENUM"):
                missing_attributes.append("_PRIM_TRUE_ENUM")
            if not hasattr(cls, "_ALT_TRUE_ENUMS"):
                missing_attributes.append("_ALT_TRUE_ENUMS")
            if not hasattr(cls, "_PRIM_FALSE_ENUM"):
                missing_attributes.append("_PRIM_FALSE_ENUM")
            if not hasattr(cls, "_ALT_FALSE_ENUMS"):
                missing_attributes.append("_ALT_FALSE_ENUMS")

            has_alternates: bool = len(missing_attributes) == 0

            

            
        
        alt_option_attribute_count: int = 0

        if hasattr(cls, "_PRIM_TRUE_ENUM"):
            alt_option_attribute_count += 1

        if hasattr(cls, "_ALT_TRUE_ENUMS"):
            alt_option_attribute_count += 1

        if

        has_alternates: bool = \
                hasattr(cls, "_PRIM_TRUE_ENUM")  \
            and hasattr(cls, "_ALT_TRUE_ENUMS")  \
            and hasattr(cls, "_PRIM_FALSE_ENUM") \
            and hasattr(cls, "_ALT_FALSE_ENUMS")

        for member in cls:
            if member.value is True:
                assert  cls._TRUE_ENUM is None         \
                    or  cls._PRIM_TRUE_ENUM is member  \
                    and cls._ALT_TRUE_ENUMS is member, \
                    f"Multiple True members found in {cls.__name__}"

                if cl
                cls._TRUE_ENUM = member
            elif member.value is False:
                assert cls._FALSE_ENUM is None, \
                    f"Multiple False members found in {cls.__name__}"
                cls._FALSE_ENUM = member

        # Ensure the subclass has defined the required class variables.
        assert hasattr(cls, "_TRUE_STRING"),   f"Class {cls.__name__} must define _TRUE_STRING"
        assert hasattr(cls, "_FALSE_STRING"),  f"Class {cls.__name__} must define _FALSE_STR"
        assert hasattr(cls, "_TRUE_STRINGS"),  f"Class {cls.__name__} must define _TRUE_STRINGS"
        assert hasattr(cls, "_FALSE_STRINGS"), f"Class {cls.__name__} must define _FALSE_STRINGS"

        assert cls._TRUE_STRING in cls._TRUE_STRINGS,   \
            f"Class {cls.__name__} _TRUE_STRING must be in _TRUE_STRINGS"
        assert cls._FALSE_STRING in cls._FALSE_STRINGS, \
            f"Class {cls.__name__} _FALSE_STRING must be in _FALSE_STRINGS"

        cls._ALL_STRS: tuple = (
            *cls._TRUE_STRINGS,
            *cls._FALSE_STRINGS,
        )

        # Build a combined mapping.
        cls._ALL_BOOL_MAP: Dict[str, bool] = {
            **{val: True  for val in cls._TRUE_STRINGS},
            **{val: False for val in cls._FALSE_STRINGS},
        }

        cls._ALL_ENUM_MAP: Dict[str, Self] = {
            **{val: cls._TRUE_ENUM  for val in cls._TRUE_STRINGS},
            **{val: cls._FALSE_ENUM for val in cls._FALSE_STRINGS},
        }

    @classmethod
    def is_true(cls, string: str) -> bool:
        """
        Check if the given string is a valid representation of True.

        This method checks if the string is in the set of True values
        defined in the subclass. It ignores leading and trailing whitespace.
        It is case-sensitive.

        Args:
            string: The string to check.

        Returns:
            bool: True if the string is a valid representation of True, False otherwise.
        """
        return string.strip() in cls._TRUE_STRINGS

    @classmethod
    def is_false(cls, string: str) -> bool:
        """
        Check if the given string is a valid representation of False.

        This method checks if the string is in the set of False values
        defined in the subclass. It ignores leading and trailing whitespace.
        It is case-sensitive.

        Args:
            string: The string to check.

        Returns:
            bool: True if the string is a valid representation of False, False otherwise.
        """
        return string.strip() in cls._FALSE_STRINGS

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
