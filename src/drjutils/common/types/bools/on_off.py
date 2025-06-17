"""
# on_off.py

## drjutils.common.bools.on_off

### Summary

This module defines the `OnOff` class, which is an enumeration representing True/False values.

### Class: OnOff

This class provides methods to validate and interpret on/off values.
It inherits from `BooleanAlias`, which is a base class for boolean-like enumerations.

### Enum Values

* `ON`:     Represents a "on" value.
* `OFF`:    Represents a "off" value.

### Attributes

* `ON_VALUES`:  Allowed strings for True values.
* `OFF_VALUES`: Allowed strings for False values.

### Private Attributes

* `_TRUE_VALUES_`:  Allowed strings for True values.
* `_FALSE_VALUES_`: Allowed strings for False values.
* `_TRUE_STR_`:     Display text for True alias.
* `_FALSE_STR_`:    Display text for False alias.

Copyright 2025 Daniel Robert Jackson
"""

"""
Standard Libraries
"""
from typing import Final, Tuple

"""
Project Libraries
"""
from drjutils.common.bools import BooleanAlias

class OnOff(BooleanAlias):
    """
    Enum class representing On/Off values.

    This class provides methods to validate and interpret on/off values.

    ### Enum Values:

    |  Enum |   Bool  | String | Alternate Strings | Description               |
    |:-----:|:-------:|:------:|:-----------------:|:--------------------------|
    |  `ON` |  `True` |  `On`  |   `on` \| `ON`    | Represents a `On` value.  |
    | `OFF` | `False` | `Off`  |  `off` \| `OFF`   | Represents a `Off` value. |

    ### Attributes:

    | Attribute Name |    Type    | Description                       |
    |:--------------:|:----------:|:----------------------------------|
    |   `ON_VALUES`  | Tuple[str] | Allowed strings for `on` values.  |
    |  `OFF_VALUES`  | Tuple[str] | Allowed strings for `off` values. |

    #### Private Attributes:

    | Attribute Name |    Type    | Description                       |
    |:--------------:|:----------:|:----------------------------------|
    |  _TRUE_VALUES_ | Tuple[str] | Allowed strings for True values.  |
    | _FALSE_VALUES_ | Tuple[str] | Allowed strings for False values. |
    |   _TRUE_STR_   |    str     | Display text for True alias.      |
    |  _FALSE_STR_   |    str     | Display text for False alias.     |
    """

    ON:  bool = True
    OFF: bool = False

    _ON_STRINGS:  Final[Tuple[str]] = ["On",  "on",  "ON"]
    _OFF_STRINGS: Final[Tuple[str]] = ["Off", "off", "OFF"]
