"""
# Daniel's Bool String Utilities

This module provides utilities for working with boolean strings.

Copyright 2025 Daniel Robert Jackson

### Constants:

| Constant                   | Type         | Description                                   |
|----------------------------|--------------|-----------------------------------------------|
| `TRUE_RXS`                 | `str`        | True Regex String                             |
| `TRUE_RGX`                 | `re.Pattern` | True Regex Pattern                            |
| `FALSE_RXS`                | `str`        | False Regex String                            |
| `FALSE_RGX`                | `re.Pattern` | False Regex Pattern                           |
| `BOOL_RXS`                 | `str`        | Boolean Regex String                          |
| `BOOL_RGX`                 | `re.Pattern` | Boolean Regex                                 |
| `YES_RXS`                  | `str`        | Yes Regex String                              |
| `YES_RGX`                  | `re.Pattern` | Yes Regex Pattern                             |
| `NO_RXS`                   | `str`        | No Regex String                               |
| `NO_RGX`                   | `re.Pattern` | No Regex Pattern                              |
| `YES_NO_RXS`               | `str`        | Yes/No Regex String                           |
| `YES_NO_RGX`               | `re.Pattern` | Yes/No Regex Pattern                          |
| `ON_RXS`                   | `str`        | On Regex String                               |
| `ON_RGX`                   | `re.Pattern` | On Regex Pattern                              |
| `OFF_RXS`                  | `str`        | Off Regex String                              |
| `OFF_RGX`                  | `re.Pattern` | Off Regex Pattern                             |
| `ON_OFF_RXS`               | `str`        | On/Off Regex String                           |
| `ON_OFF_RGX`               | `re.Pattern` | On/Off Regex Pattern                          |
| `ENABLE_RXS`               | `str`        | Enable Regex String                           |
| `ENABLE_RGX`               | `re.Pattern` | Enable Regex Pattern                          |
| `DISABLE_RXS`              | `str`        | Disable Regex String                          |
| `DISABLE_RGX`              | `re.Pattern` | Disable Regex Pattern                         |
| `ENABLE_DISABLE_RXS`       | `str`        | Enable/Disable Regex String                   |
| `ENABLE_DISABLE_RGX`       | `re.Pattern` | Enable/Disable Regex Pattern                  |
| `ENABLED_RXS`              | `str`        | Enabled Regex String                          |
| `ENABLED_RGX`              | `re.Pattern` | Enabled Regex Pattern                         |
| `DISABLED_RXS`             | `str`        | Disabled Regex String                         |
| `DISABLED_RGX`             | `re.Pattern` | Disabled Regex Pattern                        |
| `ENABLED_DISABLED_RXS`     | `str`        | Enabled/Disabled Regex String                 |
| `ENABLED_DISABLED_RGX`     | `re.Pattern` | Enabled/Disabled Regex Pattern                |
| `ENABLEDISH_RXS`           | `str`        | Enabled/Disabled Like Regex String            |
| `ENABLEDISH_RGX`           | `re.Pattern` | Enabled/Disabled Like Regex Pattern           |
| `DISABLEDISH_RXS`          | `str`        | Disabled/Enabled Like Regex String            |
| `DISABLEDISH_RGX`          | `re.Pattern` | Disabled/Enabled Like Regex Pattern           |
| `ENABLED_DISABLEDISH_RXS`  | `str`        | Enabled/Disabled Like Regex String            |
| `ENABLED_DISABLEDISH_RGX`  | `re.Pattern` | Enabled/Disabled Like Regex Pattern           |
| `TRUEISH_RXS`              | `str`        | True Regex String                             |
| `TRUEISH_RGX`              | `re.Pattern` | True Regex Pattern                            |
| `FALSEISH_RXS`             | `str`        | False Regex String                            |
| `FALSEISH_RGX`             | `re.Pattern` | False Regex Pattern                           |
| `BOOLISH_RXS`              | `str`        | Boolean Regex String                          |
| `BOOLISH_RGX`              | `re.Pattern` | Boolean Regex Pattern                         |
| `BOOLISH_PATTERN_MAP`      | `dict`       | Map of regex patterns to related values       |
| `BOOLISH_PATTERN_STR_MAP`  | `dict`       | Map of regex patterns to their string values  |
| `BOOLISH_PATTERN_BOOL_MAP` | `dict`       | Map of regex patterns to their boolean values |

### Functions:

| Function                  | Description                                                  |
|---------------------------|--------------------------------------------------------------|
| `is_bool`                 | Indicate if a string represents a boolean                    |
| `is_true`                 | Indicate if a string represents a true value                 |
| `is_true_val`             | Indicate if a value represents a true value                  |
| `is_false`                | Indicate if a string represents a false value                |
| `is_false_val`            | Indicate if a value represents a false value                 |
| `is_yes`                  | Indicate if a string represents a yes value                  |
| `is_no`                   | Indicate if a string represents a no value                   |
| `is_yes_no`               | Indicate if a string represents a yes/no value               |
| `is_on`                   | Indicate if a string represents a on value                   |
| `is_off`                  | Indicate if a string represents a off value                  |
| `is_on_off`               | Indicate if a string represents a on/off value               |
| `is_enabled`              | Indicate if a string represents a enabled value              |
| `is_disabled`             | Indicate if a string represents a disabled value             |
| `is_enabled_disabled`     | Indicate if a string represents a enabled/disabled value     |
| `is_boolish`              | Indicate if a string represents a booleanish value           |
| `is_boolish_val`          | Indicate if a value represents a booleanish value            |
| `is_trueish`              | Indicate if a string represents a trueish value              |
| `is_trueish_val`          | Indicate if a value represents a trueish value               |
| `is_falseish`             | Indicate if a string represents a falseish value             |
| `is_falseish_val`         | Indicate if a value represents a falseish value              |
| `check_true`              | Validate that a string represents a true value               |
| `check_true_val`          | Validate that a value represents a true value                |
| `check_false`             | Validate that a string represents a false value              |
| `check_false_val`         | Validate that a value represents a false value               |
| `check_bool`              | Validate that a string represents a boolean                  |
| `check_yes`               | Validate that a string represents a yes value                |
| `check_no`                | Validate that a string represents a no value                 |
| `check_yes_no`            | Validate that a string represents a yes/no value             |
| `check_on`                | Validate that a string represents a on value                 |
| `check_off`               | Validate that a string represents a off value                |
| `check_on_off`            | Validate that a string represents a on/off value             |
| `check_enabled`           | Validate that a string represents a enabled value            |
| `check_disabled`          | Validate that a string represents a disabled value           |
| `check_enabled_disabled`  | Validate that a string represents a enabled/disabled value   |
| `check_boolish`           | Validate that a string represents a booleanish value         |
| `check_boolish_val`       | Validate that a value represents a booleanish value          |
| `check_trueish`           | Validate that a string represents a trueish value            |
| `check_trueish_val`       | Validate that a value represents a trueish value             |
| `check_falseish`          | Validate that a string represents a falseish value           |
| `check_falseish_val`      | Validate that a value represents a falseish value            |
| `to_bool`                 | Convert a string to a boolean                                |
| `interpret_as_bool`       | Interpret a value as a boolean                               |
| `to_bool_str`             | Create a string formatted as a boolean (True/False) string   |
| `to_yes_no_str`           | Create a string formatted as a Yes/No string                 |
| `to_on_off_str`           | Create a string formatted as a On/Off string                 |
| `to_enabled_disabled_str` | Create a string formatted as a Enabled/Disabled string       |
| `to_std_boolish_str`      | Create a string formatted as the canonical booleanish string |
"""

"""
Standard Libraries
"""
from enum import Enum
from re import compile
from typing import Dict, Final, Pattern, Tuple, Union

__all__ = [
    # Enums #
    YesNo,                      # Yes/No Enum
    OnOff,                      # On/Off Enum
    EnabledDisabled,            # Enabled/Disabled Enum
    # Constants #
    "TRUE_RXS"                  # True Regex String
    "TRUE_RGX"                  # True Regex Pattern
    "FALSE_RXS"                 # False Regex String
    "FALSE_RGX"                 # False Regex Pattern
    "BOOL_RXS"                  # Boolean Regex String
    "BOOL_RGX"                  # Boolean Regex
    "YES_RXS"                   # Yes Regex String
    "YES_RGX"                   # Yes Regex Pattern
    "NO_RXS"                    # No Regex String
    "NO_RGX"                    # No Regex Pattern
    "YES_NO_RXS"                # Yes/No Regex String
    "YES_NO_RGX"                # Yes/No Regex Pattern
    "ON_RXS"                    # On Regex String
    "ON_RGX"                    # On Regex Pattern
    "OFF_RXS"                   # Off Regex String
    "OFF_RGX"                   # Off Regex Pattern
    "ON_OFF_RXS"                # On/Off Regex String
    "ON_OFF_RGX"                # On/Off Regex Pattern
    "ENABLED_RXS"               # Enabled Regex String
    "ENABLED_RGX"               # Enabled Regex Pattern
    "DISABLED_RXS"              # Disabled Regex String
    "DISABLED_RGX"              # Disabled Regex Pattern
    "ENABLED_DISABLED_RXS"      # Enabled/Disabled Regex String
    "ENABLED_DISABLED_RGX"      # Enabled/Disabled Regex Pattern
    "TRUEISH_RXS"               # True Regex String
    "TRUEISH_RGX"               # True Regex Pattern
    "FALSEISH_RXS"              # False Regex String
    "FALSEISH_RGX"              # False Regex Pattern
    "BOOLISH_RXS"               # Boolean Regex String
    "BOOLISH_RGX"               # Boolean Regex Pattern
    "BOOLISH_PATTERN_MAP"       # Map of regex patterns to their boolean values
    # Functions #
    "is_bool"                   # Indicate if a string represents a boolean
    "is_true"                   # Indicate if a string represents a true value
    "is_true_val"               # Indicate if a value represents a true value
    "is_false"                  # Indicate if a string represents a false value
    "is_false_val"              # Indicate if a value represents a false value
    "is_yes"                    # Indicate if a string represents a yes value
    "is_no"                     # Indicate if a string represents a no value
    "is_yes_no"                 # Indicate if a string represents a yes/no value
    "is_on"                     # Indicate if a string represents a on value
    "is_off"                    # Indicate if a string represents a off value
    "is_on_off"                 # Indicate if a string represents a on/off value
    "is_enabled"                # Indicate if a string represents a enabled value
    "is_disabled"               # Indicate if a string represents a disabled value
    "is_enabled_disabled"       # Indicate if a string represents a enabled/disabled value
    "is_boolish"                # Indicate if a string represents a booleanish value
    "is_boolish_val"            # Indicate if a value represents a booleanish value
    "is_trueish"                # Indicate if a string represents a trueish value
    "is_trueish_val"            # Indicate if a value represents a trueish value
    "is_falseish"               # Indicate if a string represents a falseish value
    "is_falseish_val"           # Indicate if a value represents a falseish value
    "check_true"                # Validate that a string represents a true value
    "check_true_val"            # Validate that a value represents a true value
    "check_false"               # Validate that a string represents a false value
    "check_false_val"           # Validate that a value represents a false value
    "check_bool"                # Validate that a string represents a boolean
    "check_yes"                 # Validate that a string represents a yes value
    "check_no"                  # Validate that a string represents a no value
    "check_yes_no"              # Validate that a string represents a yes/no value
    "check_on"                  # Validate that a string represents a on value
    "check_off"                 # Validate that a string represents a off value
    "check_on_off"              # Validate that a string represents a on/off value
    "check_enabled"             # Validate that a string represents a enabled value
    "check_disabled"            # Validate that a string represents a disabled value
    "check_enabled_disabled"    # Validate that a string represents a enabled/disabled value
    "check_boolish"             # Validate that a string represents a booleanish value
    "check_boolish_val"         # Validate that a value represents a booleanish value
    "check_trueish"             # Validate that a string represents a trueish value
    "check_trueish_val"         # Validate that a value represents a trueish value
    "check_falseish"            # Validate that a string represents a falseish value
    "check_falseish_val"        # Validate that a value represents a falseish value
    "to_bool"                   # Convert a string to a boolean
    "interpret_as_bool"         # Interpret a value as a boolean
    "to_bool_str"               # Create a string formatted as a boolean (True/False) string
    "to_yes_no_str"             # Create a string formatted as a Yes/No string
    "to_on_off_str"             # Create a string formatted as a On/Off string
    "to_enabled_disabled_str"   # Create a string formatted as a Enabled/Disabled string
    "to_std_boolish_str"        # Create a string formatted as the canonical booleanish string
]

########## Constants ##########

TRUE_RXS: Final[str] = r"[tT](?:rue)?|TRUE"
r"""
### True Regex String

*   Words: `true`, `True`, `TRUE`
*   Abrevs: `t`, `T`
*   Usage: `re.compile(TRUE_RXS)`

### Pattern: `[tT](?:rue)?|TRUE`

#### True Regex Options: `...|...`

| Opt |      Regex     |   Body | Suffix? |   Abrevs   |       Words      |  Bool  |
|----:|----------------|-------:|:--------|:----------:|:----------------:|:------:|
|   1 | `[tT](?:rue)?` | `[tT]` | `rue`   | `t` \| `T` | `true` \| `True` | `True` |
|   2 | `TRUE`         | `TRUE` |         |            |      `TRUE`      | `True` |

See also:
    | Regex Strings | Regex Patterns |
    |---------------|----------------|
    |               | `TRUE_RGX`     |
    | `FALSE_RXS`   | `FALSE_RGX`    |
    | `BOOL_RXS`    | `BOOL_RGX`     |
    | `TRUEISH_RXS` | `TRUEISH_RGX`  |
    | `FALSEISH_RXS`| `FALSEISH_RGX` |
    | `BOOLISH_RXS` | `BOOLISH_RGX`  |
"""

TRUE_RGX: Final[Pattern] = compile(rf"^\s*\b({TRUE_RXS})\b\s*$")
r"""
### True Regex Pattern

*   Words: `true`, `True`, `TRUE`
*   Abrevs: `t`, `T`
*   Usage: `re.compile(TRUE_RXS)`

### Pattern: `^\s*\b(t(?:rue)?|TRUE)\b\s*$`

#### True Regex Structure:

|  Prefix? |  (Cap Opts)  | Suffix?  |
|---------:|:------------:|:---------|
| `^\s*\b` | `(...\|...)` | `\b\s*$` |

#### True Regex Capture Options: `(...|...)`

| Opt |      Regex     |   Body | Suffix? |   Abrevs   |       Words      |  Bool  |
|----:|----------------|-------:|:--------|:----------:|:----------------:|:------:|
|   1 | `[tT](?:rue)?` | `[tT]` | `rue`   | `t` \| `T` | `true` \| `True` | `True` |
|   2 | `TRUE`         | `TRUE` |         |            |      `TRUE`      | `True` |

See also:
    | Regex Strings | Regex Patterns |
    |---------------|----------------|
    | `TRUE_RXS`    |                |
    | `FALSE_RXS`   | `FALSE_RGX`    |
    | `BOOL_RXS`    | `BOOL_RGX`     |
    | `TRUEISH_RXS` | `TRUEISH_RGX`  |
    | `FALSEISH_RXS`| `FALSEISH_RGX` |
    | `BOOLISH_RXS` | `BOOLISH_RGX`  |
"""

FALSE_RXS: Final[str] = r"[fF](?:alse)?|FALSE"
r"""
### False Regex String

*   Words: `false`, `False`, `FALSE`
*   Abrevs: `f`, `F`
*   Usage: `re.compile(FALSE_RXS)`

### Pattern: `[fF](?:alse)?|FALSE`

#### False Regex Options: `...|...`

| Opt |      Regex      |    Body | Suffix? |   Abrevs   |        Words       |   Bool  |
|----:|-----------------|--------:|:--------|:----------:|:------------------:|:-------:|
|   1 | `[fF](?:alse)?` |  `[fF]` | `alse`  | `f` \| `F` | `false` \| `False` | `False` |
|   2 | `FALSE`         | `FALSE` |         |            |       `FALSE`      | `False` |

See also:
    | Regex Strings | Regex Patterns |
    |---------------|----------------|
    | `TRUE_RXS`    | `TRUE_RGX`     |
    |               | `FALSE_RGX`    |
    | `BOOL_RXS`    | `BOOL_RGX`     |
    | `TRUEISH_RXS` | `TRUEISH_RGX`  |
    | `FALSEISH_RXS`| `FALSEISH_RGX` |
    | `BOOLISH_RXS` | `BOOLISH_RGX`  |
"""

FALSE_RGX: Final[Pattern] = compile(rf"^\s*\b({FALSE_RXS})\b\s*$")
r"""
### False Regex Pattern

*   Words: `false` | `False` | `FALSE`
*   Abrevs: `f` | `F`
*   Usage: `FALSE_RGX.match("false")`

### Pattern: `^\s*\b([fF](?:alse)?|FALSE)\b\s*$`

#### False Regex Structure:

|  Prefix? |  (Cap Opts)  | Suffix?  |
|---------:|:------------:|:---------|
| `^\s*\b` | `(...\|...)` | `\b\s*$` |

#### False Regex Capture Options: `(...|...)`

| Option |      Regex      |    Body | Suffix? |   Abrevs   |        Words       |   Bool  |
|-------:|-----------------|--------:|:--------|:----------:|:------------------:|:-------:|
|      1 | `[fF](?:alse)?` |  `[fF]` | `alse`  | `f` \| `F` | `false` \| `False` | `False` |
|      2 | `FALSE`         | `FALSE` |         |            |       `FALSE`      | `False` |

See also:
    | Regex Strings | Regex Patterns |
    |---------------|----------------|
    | `TRUE_RXS`    | `TRUE_RGX`     |
    | `FALSE_RXS`   |                |
    | `BOOL_RXS`    | `BOOL_RGX`     |
    | `TRUEISH_RXS` | `TRUEISH_RGX`  |
    | `FALSEISH_RXS`| `FALSEISH_RGX` |
    | `BOOLISH_RXS` | `BOOLISH_RGX`  |
"""

BOOL_RXS: Final[str] = rf"{TRUE_RXS}|{FALSE_RXS}"
r"""
### Boolean Regex String

*   True:
    *   Words: `true`, `True`, `TRUE`
    *   Abrevs: `t`, `T`
*   False:
    *   Words: `false`, `False`, `FALSE`
    *   Abrevs: `f`, `F`
*   Usage: `re.compile(BOOL_RXS)`
*   Note: This does not support 1 or 0 because they would be ambiguous with integers


### Pattern: `[tT](?:rue)?|TRUE|[fF](?:alse)?|FALSE`

#### Boolean Regex Option Series: `...|...`

| Option |      Regex     |    Body | Suffix? |   Abrevs   |       Words       |   Bool  |
|-------:|----------------|--------:|:--------|:----------:|:-----------------:|:-------:|
|      1 | `[tT](?:rue)?` |  `[tT]` | `rue`   | `t` \| `T` |  `true` \| `True` |  `True` |
|      2 | `TRUE`         |  `TRUE` |         |            |       `TRUE`      |  `True` |
|      3 | `[fF](?:alse)?`|  `[fF]` | `alse`  | `f` \| `F` | `false` \| `False`| `False` |
|      4 | `FALSE`        | `FALSE` |         |            |       `FALSE`     | `False` |

See also:
    | Regex Strings | Regex Patterns |
    |---------------|----------------|
    | `TRUE_RXS`    | `TRUE_RGX`     |
    | `FALSE_RXS`   | `FALSE_RGX`    |
    |               | `BOOL_RGX`     |
    | `TRUEISH_RXS` | `TRUEISH_RGX`  |
    | `FALSEISH_RXS`| `FALSEISH_RGX` |
    | `BOOLISH_RXS` | `BOOLISH_RGX`  |
"""


BOOL_RGX: Final[Pattern] = compile(rf"^\s*\b({BOOL_RXS})\b\s*$")
r"""
### Boolean Regex Pattern

*   True:
    *   Words: `true`, `True`, `TRUE`
    *   Abrevs: `t`, `T`
*   False:
    *   Words: `false`, `False`, `FALSE`
    *   Abrevs: `f`, `F`
*   Usage: `re.compile(BOOL_RXS)`
*   Note: This does not support 1 or 0 because they would be ambiguous with integers

### Pattern: `^\s*\b(t(?:rue)?|TRUE|[fF](?:alse)?|FALSE)\b\s*$`

#### Boolean Regex Structure:

|  Prefix? |  (Cap Opts)  | Suffix?  |
|---------:|:------------:|:---------|
| `^\s*\b` | `(...\|...)` | `\b\s*$` |

#### Boolean Regex Capture Options: `(...|...)`

| Option |      Regex     |    Body | Suffix? |   Abrevs   |       Words       |   Bool  |
|-------:|----------------|--------:|:--------|:----------:|:-----------------:|:-------:|
|      1 | `[tT](?:rue)?` |  `[tT]` | `rue`   | `t` \| `T` |  `true` \| `True` |  `True` |
|      2 | `TRUE`         |  `TRUE` |         |            |       `TRUE`      |  `True` |
|      3 | `[fF](?:alse)?`|  `[fF]` | `alse`  | `f` \| `F` | `false` \| `False`| `False` |
|      4 | `FALSE`        | `FALSE` |         |            |       `FALSE`     | `False` |

See also:
    | Regex Strings | Regex Patterns |
    |---------------|----------------|
    | `TRUE_RXS`    | `TRUE_RGX`     |
    | `FALSE_RXS`   | `FALSE_RGX`    |
    | `BOOL_RXS`    |                |
    | `TRUEISH_RXS` | `TRUEISH_RGX`  |
    | `FALSEISH_RXS`| `FALSEISH_RGX` |
    | `BOOLISH_RXS` | `BOOLISH_RGX`  |
"""



class YesNo(Enum):
    """
    Yes/No Enum

    This enum represents the Yes/No values.
    """
    Yes = True
    No  = False

    def __str__(self) -> str:
        """
        Convert the enum value to a string.

        Returns:
            str: The string representation of the enum value.
        """
        return "Yes" if self.value else "No"

    YES_RXS: Final[str] = r"y(?:es)?"
    r"""
    ### Yes Regex String
    
    *   Words: `yes`, `Yes`, `YES`
    *   Abbrevs: `y`, `Y`
    *   Usage: `re.compile(YES_RXS)`
    
    ### Pattern: `y(?:es)?`
    
    #### Yes Regex Structure:
    
    |    Regex   | Letter | Suffix? | Value |
    |------------|-------:|:--------|-------|
    | `y(?:es)?` |    `y` | `es`    | True  |
    
    See also:
        | Regex Strings | Regex Patterns |
        |---------------|----------------|
        |               | `YES_RGX`      |
        | `NO_RXS`      | `NO_RGX`       |
        | `YES_NO_RXS`  | `YES_NO_RGX`   |
        | `TRUEISH_RXS` | `TRUEISH_RGX`  |
        | `FALSEISH_RXS`| `FALSEISH_RGX` |
        | `BOOLISH_RXS` | `BOOLISH_RGX`  |
    """
    
    YES_RGX: Final[Pattern] = compile(rf"^\s*\b({YES_RXS})\b\s*$")
    r"""
    ### Yes Regex Pattern
    
    *   e.g.: `y`, `Y`, `yes`, `Yes`, `YES`, etc.
    *   Usage: `YES_RGX.match("yes")`
    
    ### Pattern: `^\s*(y(?:es)?)\s*$`
    
    #### Yes Regex Structure:
    
    |  Prefix? | (Cap Grp) | Suffix?  |
    |---------:|:---------:|:---------|
    | `^\s*\b` |  `(...)`  | `\b\s*$` |
    
    #### Yes Regex Capture Group: `(...)`
    
    |    Regex   | Letter | Suffix? | Value |
    |------------|-------:|:--------|-------|
    | `y(?:es)?` |    `y` | `es`    | True  |
    
    See also:
        | Regex Strings | Regex Patterns |
        |---------------|----------------|
        | `YES_RXS`     |                |
        | `NO_RXS`      | `NO_RGX`       |
        | `YES_NO_RXS`  | `YES_NO_RGX`   |
        | `TRUEISH_RXS` | `TRUEISH_RGX`  |
        | `FALSEISH_RXS`| `FALSEISH_RGX` |
        | `BOOLISH_RXS` | `BOOLISH_RGX`  |
    """
    
    NO_RXS: Final[str] = r"no?"
    r"""
    ### No Regex String
    
    *   e.g.: `n`, `N`, `no`, `No`, `NO`, etc.
    *   Usage: `re.compile(NO_RXS)`
    
    ### Pattern: `no?`
    
    #### No Regex Structure:
    
    | Regex | Letter | Suffix? | Value |
    |-------|-------:|:--------|-------|
    | `no?` |    `n` | `o`     | False |
    
    
    See also:
        | Regex Strings | Regex Patterns |
        |---------------|----------------|
        | `YES_RXS`     | `YES_RGX`      |
        |               | `NO_RGX`       |
        | `YES_NO_RXS`  | `YES_NO_RGX`   |
        | `TRUEISH_RXS` | `TRUEISH_RGX`  |
        | `FALSEISH_RXS`| `FALSEISH_RGX` |
        | `BOOLISH_RXS` | `BOOLISH_RGX`  |
    """
    
    NO_RGX: Final[Pattern] = compile(rf"^\s*\b({NO_RXS})\b\s*$")
    r"""
    ### No Regex Pattern
    
    *   e.g.: `n`, `N`, `no`, `No`, `NO`, etc.
    *   Usage: `NO_RGX.match("no")`
    
    ### Pattern: `^\s*(no?)\s*$`
    
    #### No Regex Structure:
    
    |  Prefix? | (Cap Grp) | Suffix?  |
    |---------:|:---------:|:---------|
    | `^\s*\b` |  `(...)`  | `\b\s*$` |
    
    #### No Regex Capture Group: `(...)`
    
    | Regex | Letter | Suffix? | Value |
    |-------|-------:|:--------|-------|
    | `no?` |    `n` | `o`     | False |
    
    See also:
        | Regex Strings | Regex Patterns |
        |---------------|----------------|
        | `YES_RXS`     | `YES_RGX`      |
        | `NO_RXS`      |                |
        | `YES_NO_RXS`  | `YES_NO_RGX`   |
        | `TRUEISH_RXS` | `TRUEISH_RGX`  |
        | `FALSEISH_RXS`| `FALSEISH_RGX` |
        | `BOOLISH_RXS` | `BOOLISH_RGX`  |
    """
    
    YES_NO_RXS: Final[str] = rf"{YES_RXS}|{NO_RXS}"
    r"""
    ### Yes/No Regex String
    
    *   Yes
        *   e.g.: `y`, `Y`, `yes`, `Yes`, `YES`, etc.
    *   No
        *   e.g.: `n`, `N`, `no`, `No`, `NO`, etc.
    *   Usage: `re.compile(YES_NO_RXS)`
    
    ### Pattern: `y(?:es)?|no?`
    
    #### Yes/No Regex Option Series: `...|...`
    
    | Option |    Regex   | Letter | Suffix? | Value |
    |-------:|------------|-------:|:--------|-------|
    |      1 | `y(?:es)?` |    `y` | `es`    | True  |
    |      2 | `no?`      |    `n` | `o`     | False |
    
    See also:
        | Regex Strings | Regex Patterns |
        |---------------|----------------|
        | `YES_RXS`     | `YES_RGX`      |
        | `NO_RXS`      | `NO_RGX`       |
        |               | `YES_NO_RGX`   |
        | `TRUEISH_RXS` | `TRUEISH_RGX`  |
        | `FALSEISH_RXS`| `FALSEISH_RGX` |
        | `BOOLISH_RXS` | `BOOLISH_RGX`  |
    """
    
    YES_NO_RGX: Final[Pattern] = compile(rf"^\s*\b({YES_NO_RXS})\b\s*$")
    r"""
    ### Yes/No Regex Pattern
    
    *   Yes
        *   e.g.: `y`, `Y`, `yes`, `Yes`, `YES`, etc.
    *   No
        *   e.g.: `n`, `N`, `no`, `No`, `NO`, etc.
    *   Usage: `YES_NO_RGX.match("yes")`
    
    ### Pattern: `^\s*(y(?:es)?|no?)\s*$`
    
    #### Yes/No Regex Structure:
    
    |  Prefix? |  (Cap Opts)  | Suffix?  |
    |---------:|:------------:|:---------|
    | `^\s*\b` | `(...\|...)` | `\b\s*$` |
    
    #### Yes/No Regex Capture Options: `(...|...)`
    
    | Option |    Regex   | Letter | Suffix? | Value |
    |-------:|------------|-------:|:--------|-------|
    |      1 | `y(?:es)?` |    `y` | `es`    | True  |
    |      2 | `no?`      |    `n` | `o`     | False |
    
    See also:
        | Regex Strings | Regex Patterns |
        |---------------|----------------|
        | `YES_RXS`     | `YES_RGX`      |
        | `NO_RXS`      | `NO_RGX`       |
        | `YES_NO_RXS`  |                |
        | `TRUEISH_RXS` | `TRUEISH_RGX`  |
        | `FALSEISH_RXS`| `FALSEISH_RGX` |
        | `BOOLISH_RXS` | `BOOLISH_RGX`  |
    """

    @classmethod
    def interp(cls, val: Union[str, int, bool]) -> "YesNo":
        """
        Interpret a value as a Yes/No enum.

        Args:
            val (Union[str, int, bool]): The value to interpret.

        Returns:
            YesNo: The interpreted Yes/No enum value.
        """
        if isinstance(val, str):
            if YES_RGX.match(val):
                return cls.Yes
            elif NO_RGX.match(val):
                return cls.No
        elif isinstance(val, bool):
            return cls.Yes if val else cls.No
        raise ValueError(f"Cannot interpret {val} as Yes/No")

ON_RXS: Final[str] = r"[oO]n|ON"
r"""
### On Regex String

*   e.g.: `on`, `On`, `ON`, etc.

TODO: docstring
"""

ON_RGX: Final[Pattern] = compile(rf"^\s*\b({ON_RXS})\b\s*$")
r"""
TODO: docstring
"""

OFF_RXS: Final[str] = r"[oO]ff|OFF"
r"""
TODO: docstring
"""

OFF_RGX: Final[Pattern] = compile(rf"^\s*\b({OFF_RXS})\b\s*$")
r"""
TODO: docstring
"""

ON_OFF_RXS: Final[str] = rf"[oO](?:n|ff)|O(?:N|FF)"
"""
TODO: docstring
"""

ENABLE_RXS: Final[str] = r"[eE]nable|ENABLE"
r"""
TODO: docstring
"""

ENABLE_RGX: Final[Pattern] = compile(rf"^\s*\b({ENABLE_RXS})\b\s*$")
r"""
TODO: docstring
"""

DISABLE_RXS: Final[str] = r"[dD]isable|DISABLE"
r"""
TODO: docstring
"""

DISABLE_RGX: Final[Pattern] = compile(rf"^\s*\b({DISABLE_RXS})\b\s*$")
r"""
TODO: docstring
"""

ENABLE_DISABLE_RXS: Final[str] = r"(?:[eE]n|[dD]is)able|(?:EN|DIS)ABLE"
r"""
TODO: docstring
"""

ENABLE_DISABLE_RGX: Final[Pattern] = compile(rf"^\s*\b({ENABLE_DISABLE_RXS})\b\s*$")
r"""
TODO: docstring
"""

ENABLED_RXS: Final[str] = r"[eE]nabled|ENABLED"
r"""
TODO: docstring
"""

ENABLED_RGX: Final[Pattern] = compile(rf"^\s*\b({ENABLED_RXS})\b\s*$")
r"""
TODO: docstring
"""

DISABLED_RXS: Final[str] = r"[dD]isabled|DISABLED"
r"""
TODO: docstring
"""

DISABLED_RGX: Final[Pattern] = compile(rf"^\s*\b({DISABLED_RXS})\b\s*$")
r"""
TODO: docstring
"""

ENABLED_DISABLED_RXS: Final[str] = r"(?:[eE]n|[dD]is)abled|(?:EN|DIS)ABLED"
r"""
TODO: docstring
"""

ENABLED_DISABLED_RGX: Final[Pattern] = compile(rf"^\s*\b({ENABLED_DISABLED_RXS})\b\s*$")
r"""
TODO: docstring
"""

ENABLEDISH_RXS: Final[str] = r"[eE]nabled?|ENABLED?"
r"""
TODO: docstring
"""

ENABLEDISH_RGX: Final[Pattern] = compile(rf"^\s*\b({ENABLEDISH_RXS})\b\s*$")
r"""
TODO: docstring
"""

DISABLEDISH_RXS: Final[str] = r"[dD]isabled?|DISABLED?"
r"""
TODO: docstring
"""

DISABLEDISH_RGX: Final[Pattern] = compile(rf"^\s*\b({DISABLEDISH_RXS})\b\s*$")
r"""
TODO: docstring
"""

ENABLED_DISABLEDISH_RXS: Final[str] = r"(?:[eE]n|[dD]is)abled?|(?:EN|DIS)ABLED?"
r"""
TODO: docstring
"""

ENABLED_DISABLEDISH_RGX: Final[Pattern] = compile(rf"^\s*\b({ENABLED_DISABLEDISH_RXS})\b\s*$")
r"""
TODO: docstring
"""

TRUEISH_RXS: Final[str] = rf"{TRUE_RXS}|{YES_RXS}|{ON_RXS}|{ENABLEDISH_RXS}"
r"""
TODO: docstring
"""

TRUEISH_RGX: Final[Pattern] = compile(rf"^\s*\b({TRUEISH_RXS})\b\s*$")
r"""
TODO: docstring
"""

FALSEISH_RXS: Final[str] = rf"{FALSE_RXS}|{NO_RXS}|{OFF_RXS}|{DISABLEDISH_RXS}"
r"""
TODO: docstring
"""

FALSEISH_RGX: Final[Pattern] = compile(rf"^\s*\b({FALSEISH_RXS})\b\s*$")
r"""
TODO: docstring
"""

BOOLISH_RXS: Final[str] = rf"{BOOL_RXS}|{YES_NO_RXS}|{ON_OFF_RXS}|{ENABLED_DISABLEDISH_RXS}"
r"""
TODO: docstring
"""

BOOLISH_RGX: Final[Pattern] = compile(rf"^\s*\b({BOOLISH_RXS})\b\s*$")
r"""
TODO: docstring
"""

BOOLISH_PATTERN_MAP: Final[Dict[Pattern, Tuple[str, bool]]] = {
    TRUE_RGX:           ("True",        True),
    FALSE_RGX:          ("False",       False),
    YES_RGX:            ("Yes",         True),
    NO_RGX:             ("No",          False),
    ON_RGX:             ("On",          True),
    OFF_RGX:            ("Off",         False),
    ENABLEDISH_RGX:     ("Enabled",     True),
    DISABLEDISH_RGX:    ("Disabled",    False),
}
r"""
TODO: docstring
"""

BOOLISH_PATTERN_STR_MAP: Final[Dict[Pattern, str]] = {
    TRUE_RGX:           "True",
    FALSE_RGX:          "False",
    YES_RGX:            "Yes",
    NO_RGX:             "No",
    ON_RGX:             "On",
    OFF_RGX:            "Off",
    ENABLEDISH_RGX:     "Enabled",
    DISABLEDISH_RGX:    "Disabled",
}
r"""
TODO: docstring
"""

BOOLISH_PATTERN_BOOL_MAP: Final[Dict[Pattern, bool]] = {
    TRUE_RGX:           True,
    FALSE_RGX:          False,
    YES_RGX:            True,
    NO_RGX:             False,
    ON_RGX:             True,
    OFF_RGX:            False,
    ENABLEDISH_RGX:     True,
    DISABLEDISH_RGX:    False,
}
r"""
TODO: docstring
"""

########## Functions ##########

def is_bool_str(string: str) -> bool:
    """
    Determine if the string represents a boolean value.
    
    Args:
        string (str): The string to evaluate.
        
    Returns:
        bool: True if the string represents a boolean value, False otherwise.
    """
    return BOOL_RGX.match(string)is not None

def is_boolish_str(string: str) -> bool:
    """
    Determine if the string represents a boolean value or can be interpreted as a boolean.
    
    Args:
        string (str): The string to evaluate.
        
    Returns:
        bool: True if the string represents a booleanish value, False otherwise.
    """
    return BOOLISH_RGX.match(string)is not None




def to_bool(num: Union[str, Number]) -> bool:
    """
    Convert a string that represents a boolean value or a number to a boolean.
    
    Does 
    Also accepts numbers as input just to be more flexible. Just returns the number as-is.

    Args:
        num (Union[str, Number]): The string to convert.

    Returns:
        Union[int, float]: The converted number.
    """
    if is_real(num):
        return float(num)
    elif is_int(num):
        return int(num) if is_int_dec(num) else 

    raise ValueError(f"Invalid number format: {num}")


def to_bool_str(value: Union[Number, str]) -> str:
    """
    Format as a boolean string
    values: `True` or `False`
    
    Args:
        value (Union[Number, str]): The boolean interpretable value to format.
        
    Returns:
        str: The formatted boolean value as a string.
    """
    if not isinstance(value, bool):
        value = interpret_as_bool(value)
        
    return str(value)