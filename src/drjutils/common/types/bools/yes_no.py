"""
# yes_no.py

## drjutils.common.bools.yes_no

### Summary

This module defines the `YesNo` class, which is an enumeration representing True/False values.

### Class: YesNo

This class provides methods to validate and interpret yes/no values.
It inherits from `BooleanAlias`, which is a base class for boolean-like enumerations.

### Enum Values

* `YES`:    Represents a "yes" value.
* `NO`:     Represents a "no" value.

### Attributes

* `YES_VALUES`: Allowed strings for True values.
* `NO_VALUES`:  Allowed strings for False values.

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

class YesNo(BooleanAlias):
    """
    Enum class representing Yes/No values.

    This class provides methods to validate and interpret yes/no values.

    ### Enum Values:

    |  Enum |   Bool  | String |       Alternate Strings      | Description               |
    |:-----:|:-------:|:------:|:----------------------------:|:--------------------------|
    | `YES` |  `True` |  `Yes` | `y` \| `Y` \| `yes` \| `YES` | Represents a `Yes` value. |
    |  `NO` | `False` |   `No` |  `n` \| `N` \| `no` \| `NO`  | Represents a `No` value.  |

    ### Attributes:

    | Attribute Name |    Type    | Description                       |
    |:--------------:|:----------:|:----------------------------------|
    |  `YES_VALUES`  | Tuple[str] | Allowed strings for `yes` values. |
    |   `NO_VALUES`  | Tuple[str] | Allowed strings for `no` values.  |

    #### Private Attributes:

    | Attribute Name |    Type    | Description                       |
    |:--------------:|:----------:|:----------------------------------|
    |  _TRUE_VALUES_ | Tuple[str] | Allowed strings for True values.  |
    | _FALSE_VALUES_ | Tuple[str] | Allowed strings for False values. |
    |   _TRUE_STR_   |    str     | Display text for True alias.      |
    |  _FALSE_STR_   |    str     | Display text for False alias.     |
    """

    YES = True
    NO  = False

    YES_VALUES: Final[Tuple[str]] = ["y", "Y", "yes", "Yes", "YES"]
    NO_VALUES:  Final[Tuple[str]] = ["n", "N", "no", "No", "NO"]

    _TRUE_VALUES_:  Final[Tuple[str]] = YES_VALUES
    _FALSE_VALUES_: Final[Tuple[str]] = NO_VALUES
    _TRUE_STR_:     Final[str] = "Yes"
    _FALSE_STR_:    Final[str] = "No"
