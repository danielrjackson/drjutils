"""
# Daniel's Signs Module

This module provides utilities for working with signs in strings.

Copyright 2025 Daniel Robert Jackson

### Attributes:

| Attribute     | Type         | Description                                          |
|---------------|--------------|------------------------------------------------------|
| `NEG_RGX`     | `re.Pattern` | Negative Symbol Regex Pattern                        |
| `NEG_RXS`     | `str`        | Negative Symbol Regex String                         |
| `POS_RGX`     | `re.Pattern` | Positive Symbol Regex Pattern                        |
| `POS_RXS`     | `str`        | Positive Symbol Regex String                         |
| `POS_OPT_RXS` | `str`        | Optional Positive Symbol Regex String (Not Negative) |
| `SGN_RGX`     | `re.Pattern` | Sign Symbol Regex Pattern                            |
| `SGN_RXS`     | `str`        | Sign Symbol Regex String                             |
| `SGN_OPT_RXS` | `str`        | Optional Sign Symbol Regex String                    |

### Functions:

| Function             | Description                                                   |
|----------------------|---------------------------------------------------------------|
| `check_has_neg()`    | Check if a string starts with a negative sign (`-`)           |
| `check_has_pos()`    | Check if a string starts with a positive sign (`+`)           |
| `check_signed()`     | Check if a string starts with a sign (`+` or `-`)             |
| `has_neg()`          | Check if a string starts with a negative sign (`-`)           |
| `has_pos()`          | Check if a string starts with a positive sign (`+`)           |
| `is_signed()`        | Check if a string starts with a sign (`+` or `-`)             |
"""

"""
Standard Libraries
"""
from numbers import Number
from re import compile
from typing import Final, Pattern, Union

__all__ = [
    # Attributes #
    "NEG_RGX",       # Negative Regex Pattern
    "NEG_RXS",       # Negative Regex String
    "POS_RGX",       # Positive Regex Pattern
    "POS_RXS",       # Positive Regex String
    "POS_OPT_RXS",   # Optional Positive (And Not Negative) Regex String
    "SGN_RGX",       # Sign Regex Pattern
    "SGN_RXS",       # Sign Regex String
    "SGN_OPT_RXS",   # Optional Sign Regex String
    # Functions #
    "check_has_neg", # Check if a string starts with a negative sign (`-`)
    "check_has_pos", # Check if a string starts with a positive sign (`+`)
    "check_signed",  # Check if a string starts with a sign (`+` or `-`)
    "has_neg",       # Indicate if a string starts with a negative sign (`-`)
    "has_pos",       # Indicate if a string starts with a positive sign (`+`)
    "is_signed"      # Indicate if a string starts with a sign (`+` or `-`)
]

########## Attributes ##########

NEG_RXS = Final[str] = r"-"
"""
### Negative Symbol Regex String

Indicates if the character is a negative sign (`-`).

*   Usage: `re.compile(NEG_RXS)`

### Pattern: `-`

See also:
|  Regex String | Regex Pattern | Description         |
|---------------|---------------|:--------------------|
| `NEG_RXS`     | `NEG_RGX`     | Has Negative Symbol |


|  Predicate |   Validator   | Description                               |
|------------|---------------|:------------------------------------------|
| `is_neg()` | `check_neg()` | Has Negative Symbol Or Is Negative Number |
"""

NEG_RGX = Final[Pattern] = compile(f"^\s*{NEG_RXS}")
"""
### Negative Symbol Regex Pattern

*   Usage: NEG_RGX.match("-")

### Pattern: `^\s*-`

| Prefix? | Sign |
|--------:|:-----|
|  `^\s*` | `-`  |

See also:
|  Regex String | Regex Pattern | Description         |
|---------------|---------------|:--------------------|
| `NEG_RXS`     | `NEG_RGX`     | Has Negative Symbol |

|  Predicate |   Validator   | Description         |
|------------|---------------|:--------------------|
| `is_neg()` | `check_neg()` | Has Negative Symbol |
"""

POS_RXS = Final[str] = r"\+"
"""
### Positive Symbol Regex String

Indicates if the character is a positive sign (`+`).

*   Usage: `re.compile(POS_RXS)`

### Pattern: `\+`

See also:
|  Regex String | Regex Pattern | Description                                     |
|---------------|---------------|:------------------------------------------------|
| `POS_RXS`     | `POS_RGX`     | Has Positive Symbol                             |
| `POS_OPT_RXS` |               | Has Optional Positive Symbol (And Not Negative) |

|  Predicate |   Validator   | Description         |
|------------|---------------|:--------------------|
| `is_pos()` | `check_pos()` | Has Positive Symbol |
"""

POS_RGX = compile(f"^\s*{POS_RXS}")
"""
### Positive Symbol Regex Pattern

*   Usage: POS_RGX.match("+")

### Pattern: `^\s*\+`

#### Positive Symbol Regex Structure:

| Prefix? | Sign |
|--------:|:-----|
|  `^\s*` | `\+` |

See also:
|  Regex String | Regex Pattern | Description                                     |
|---------------|---------------|:------------------------------------------------|
| `POS_RXS`     | `POS_RGX`     | Has Positive Symbol                             |
| `POS_OPT_RXS` |               | Has Optional Positive Symbol (And Not Negative) |

|  Predicate |   Validator   | Description         |
|------------|---------------|:--------------------|
| `is_pos()` | `check_pos()` | Has Positive Symbol |
"""

POS_OPT_RXS = f"(?!-){POS_RXS}?"
"""
### Optional Positive Symbol Regex String

Indicates if the character is a positive sign (`+`) or empty string.
Must not be a negative sign (`-`).

*   Usage: `re.compile(POS_OPT_RXS)`

### Pattern: `(?!-)\+?`

#### Optional Positive Symbol Regex Structure:

| Not Negative | Sign? |
|-------------:|:------|
|      `(?!-)` | `\+?` |

See also:
|  Regex String | Regex Pattern | Description                                     |
|---------------|---------------|:------------------------------------------------|
| `POS_RXS`     | `POS_RGX`     | Has Positive Symbol                             |
| `POS_OPT_RXS` |               | Has Optional Positive Symbol (And Not Negative) |

|  Predicate |   Validator   | Description         |
|------------|---------------|:--------------------|
| `is_pos()` | `check_pos()` | Has Positive Symbol |
"""

sign_RXS = r"[+-]"
"""
### Sign Regex String

*   values: `+` or `-`
*   Usage: `re.compile(sign_RXS)`

### Pattern: `[+-]`

See also: `sign_OPT_RXS`
"""

sign_OPT_RXS = r"[+-]?"
"""
### Optional Sign Regex String

*   values: `+`, `-`, or empty string
*   Usage: `re.compile(sign_OPT_RXS)`

### Pattern: `[+-]?`

See also: `sign_RXS`
"""

########## Functions ##########

def is_neg(value: str) -> bool:
    """
    Check if a string starts with a negative sign (`-`).
    
    Args:
        value (str): The string to check.
        
    Returns:

    """
    return NEG_RGX.match(value) is not None
