"""
# true_false.py

## drjutils.common.bools.true_false

### Summary

This module defines the `TrueFalse` class, which is an enumeration representing True/False values.

### Class: TrueFalse

This class provides methods to validate and interpret True/False values.
It inherits from `BooleanAlias`, which is a base class for boolean-like enumerations.

### Enum Values

* `TRUE`:   Represents a "True" value.
* `FALSE`:  Represents a "False" value.

### Attributes

* `TRUE_VALUES`:    Allowed strings for True values.
* `FALSE_VALUES`:   Allowed strings for False values.

### Private Attributes

- `_TRUE_VALUES_`:  Allowed strings for True values.
- `_FALSE_VALUES_`: Allowed strings for False values.
- `_TRUE_STR_`:     Display text for True alias.
- `_FALSE_STR_`:    Display text for False alias.

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

class TrueFalse(BooleanAlias):
    """
    Enum class representing True/False values.

    This class provides methods to validate and interpret True/False values.

    ### Enum Values:

    |   Enum  |   Bool  |  String |         Alternate Strings        | Description                 |
    |:-------:|:-------:|:-------:|:--------------------------------:|:----------------------------|
    |  `TRUE` |  `True` |  `True` |  `t` \| `T` \| `true` \| `TRUE`  | Represents a `True` value.  |
    | `FALSE` | `False` | `False` | `f` \| `F` \| `false` \| `FALSE` | Represents a `False` value. |

    ### Attributes:

    | Attribute Name |    Type    | Description                         |
    |:--------------:|:----------:|:------------------------------------|
    |  `TRUE_VALUES` | Tuple[str] | Allowed strings for `True` values.  |
    | `FALSE_VALUES` | Tuple[str] | Allowed strings for `False` values. |

    #### Private Attributes:

    | Attribute Name |    Type    | Description                       |
    |:--------------:|:----------:|:----------------------------------|
    |  _TRUE_VALUES_ | Tuple[str] | Allowed strings for True values.  |
    | _FALSE_VALUES_ | Tuple[str] | Allowed strings for False values. |
    |   _TRUE_STR_   |    str     | Display text for True alias.      |
    |  _FALSE_STR_   |    str     | Display text for False alias.     |
    """

    TRUE    = True
    FALSE   = False

    TRUE_VALUES:    Final[Tuple[str]] = ["t", "T", "true", "True", "TRUE"]
    FALSE_VALUES:   Final[Tuple[str]] = ["f", "F", "false", "False", "FALSE"]

    _TRUE_VALUES_:  Final[Tuple[str]] = TRUE_VALUES
    _FALSE_VALUES_: Final[Tuple[str]] = FALSE_VALUES
    _TRUE_STR_:     Final[str] = "True"
    _FALSE_STR_:    Final[str] = "False"
