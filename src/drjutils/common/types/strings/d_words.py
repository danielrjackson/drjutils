"""
# Daniel's Word Module

This module provides regex patterns and functions for string manipulation related to words.
The primary use case is handling different formats of strings, such as converting between them.
e.g. `camelCase`, `snake_case`, `kebab-case`, etc.

See also: [casefy](https://pypi.org/project/casefy/)

Copyright 2025 Daniel Robert Jackson

### Enumerations:

| Enumeration | Description         |
|-------------|---------------------|
| StrCase     | String Case Formats |

### Functions:

| Function | Description                            |
|----------|----------------------------------------|
| to_case  | Convert a string to the specified case |
"""

"""
Standard Libraries
"""
from enum import IntEnum
from regex import Pattern, compile
from typing import Union, Optional, Callable, Any, Final, TypeVar, Generic, Literal, overload, List
from types import FunctionType
from packaging import version

"""
Third-Party Libraries
"""
import casefy

__all__ = [
    # Enumerations #
    "StrCase",  # String Case Formats
    # Functions #
    "to_case",  # Convert a string to the specified case
]

########## Constants ##########
DIGITS_RXS: Final[str] = r"\d+"
r"""
### Regular expression for digits.

### Pattern:
`\d+`
"""

WORD_LOW_RXS: Final[str] = r"[a-z]+"
"""
### Regular expression for lowercase words.

### Pattern:
`[a-z]+`
"""

WORD_CAMEL_RXS: Final[str] = r"[A-Z][a-z]*"
"""
### Regular expression for capitalized words.

* Alphabetic words with the first letter capitalized and the rest lowercase.

### Pattern:
`[A-Z][a-z]*`

|   First | Body     |
|--------:|:---------|
| `[A-Z]` | `[a-z]*` |
"""

WORD_CAP_RXS: Final[str] = r"[A-Z]+"
"""
### Regular expression for words with all letters capitalized.

### Pattern:
`[A-Z]+`
"""

ACRO_ALPHA_RXS: Final[str] = r"[A-Z]{2,}(?![a-z])"
"""
### Regular expression for alphabetic acronyms.

* Alphabetic words with all letters capitalized.

### Pattern:
`[A-Z]{2,}(?![a-z])`

|     Acronym | NegLook LC  |
|------------:|:------------|
| `[A-Z]{2,}` | `(?![a-z])` |
"""

ACRO_ALNUM_RXS: Final[str] = r"[A-Z\d]{2,}(?![a-z])"
"""
### Regular expression for alphanumeric acronyms.

* Alphanumeric words with all letters capitalized.
* If it is followed by a capitalized word, the last capitalized letter is not included in the
  acronym.

### Pattern:
`[A-Z\d]{2,}(?![a-z])`

|       Acronym | NegLook LC  |
|--------------:|:------------|
| `[A-Z\d]{2,}` | `(?![a-z])` |
"""

ACRO_ALNUM_ALPHA_START_RXS: Final[str] = r"[A-Z][A-Z\d]+(?![a-z])"
"""
### Regular expression for alphanumeric acronyms starting with an alphabetic character.

* Alphanumeric words with all letters capitalized and starting with an alphabetic character.

### Pattern:
`[A-Z][A-Z\d]+(?![a-z])`

|   First |    Body    | NegLook LC  |
|--------:|:----------:|:------------|
| `[A-Z]` | `[A-Z\d]+` | `(?![a-z])` |
"""

ACRO_ALNUM_NUM_START_RXS: Final[str] = r"\d[A-Z\d]+(?![a-z])"
"""
### Regular expression for alphanumeric acronyms starting with a number.

* Alphanumeric words with all letters capitalized and starting with a number.

### Pattern:
`\d[A-Z\d]+`

| First |    Body    | NegLook LC  |
|------:|:----------:|:------------|
|  `\d` | `[A-Z\d]+` | `(?![a-z])` |
"""

ACRO_ALNUM_NUM_END_RXS: Final[str] = r"[A-Z\d]+\d"
"""
### Regular expression for alphanumeric acronyms ending with a number.

* Alphanumeric words with all letters capitalized and ending with a number.

### Pattern:
`[A-Z\d]+\d`

|       Body | Last |
|-----------:|:-----|
| `[A-Z\d]+` | `\d` |
"""

VER_NUM_RXS: Final[str] = r"v\d+"
"""
### Regular expression for version numbers.

* Version numbers starting with a lowercase 'v' followed by digits.
* Note: Versions are integers only. No subversion numbers.
* e.g. `v1`, `v2`, `v3`, etc.

### Pattern:
`v\d+`

| Prefix | Ver Num |
|-------:|:--------|
|    `v` | `\d+`   |
"""

BRAND_I_NAMES: Final[tuple[str, ...]] = (
    "iPhone",
    "iPad",
    "iPod",
    "iMac",
    "iMessage",
    "iCloud",
    "iTunes",
)
r"""
### Tuple of common product names starting with 'i'.

Values: `iPhone`, `iPad`, `iPod`, `iMac`, `iMessage`, `iCloud`, `iTunes`
"""

BRAND_E_NAMES: Final[tuple[str, ...]] = (
    "eMail",
    "eBook",
    "ePub",
    "eCommerce",
)
r"""
### Tuple of common product names starting with 'e'.

Values: `eMail`, `eBook`, `ePub`, `eCommerce`
"""

BRAND_X_NAMES: Final[tuple[str, ...]] = (
    "x86",
    "x64",
    "xAI",
)
r"""
### Tuple of common product names starting with 'x'.
Values: `x86`, `x64`, `xAI`
"""

BRAND_I_RXS: Final[str] = r"i(?:Phone|Pad|Pod|Mac|Message|Cloud|Tunes)"
r"""
### Regular expression for common product names starting with 'i'.

*   Designed to check only a single letter prefix first so that it can drop out if the prefix does
    not match.

### Pattern:
`i(?:Phone|Pad|Pod|Mac|Message|Cloud|Tunes)`

Regex Structure:

| Prefix | Non-Capturing Options |
|-------:|:----------------------|
|    `i` | `(?:...\|...)`        |

| Num | Option    |
|----:|:----------|
|   1 | `Phone`   |
|   2 | `Pad`     |
|   3 | `Pod`     |
|   4 | `Mac`     |
|   5 | `Message` |
|   6 | `Cloud`   |
|   7 | `Tunes`   |
"""

BRAND_E_RXS: Final[str] = r"e(?:Mail|Book|Pub|Commerce)"
r"""
### Regular expression for common product names starting with 'e'.

*   Designed to check only a single letter prefix first so that it can drop out if the prefix does
    not match.
    
### Pattern:
`e(?:Mail|Book|Pub|Commerce)`

Regex Structure: `e(?:...|...)`

| Prefix | Non-Capturing Options |
|-------:|:----------------------|
|    `e` | `(?:...\|...)`        |

| Num | Option     |
|----:|:-----------|
|   1 | `Mail`     |
|   2 | `Book`     |
|   3 | `Pub`      |
|   4 | `Commerce` |
"""

BRAND_X_RXS: Final[str] = r"x(?:86|64|AI|Unit)"
r"""
### Regular expression for common product names starting with 'x'.

*   Designed to check only a single letter prefix first so that it can drop out if the prefix does
    not match.
    
### Pattern:
`x(?:86|64|AI|Unit)`

Regex Structure: `x(?:...|...)`

| Prefix | Non-Capturing Options |
|-------:|:----------------------|
|    `x` | `(?:...\|...)`        |

| Num | Option     |
|----:|:-----------|
|   1 | `86`       |
|   2 | `64`       |
|   3 | `AI`       |
|   4 | `Unit`     |
"""

LC_BRAND_RXS: Final[str] = f"{BRAND_I_RXS}|{BRAND_E_RXS}|{BRAND_X_RXS}"
r"""
### Regular expression for common brand names starting with lowercase letters.

*   The common ones are: 'i', 'e', or 'x'.
*   The rest of the name is a capitalized word
*   Designed to check only a single letter prefix first so that it can drop out if the prefix does
    not match.

### Pattern:
`i(?:Phone|Pad|Pod|Mac|Message|Cloud|Tunes)|e(?:Mail|Book|Pub|Commerce)|x(?:86|64|AI|Unit)`

Regex Structure: Option Series (`...|...`)

Each option's structure is as follows:

|   Lower Case Prefix   | Non-Capturing Options |
|:---------------------:|:----------------------|
|   `i` \| `e` \| `x`   | `(?:...\|...)`        |

|         Group         | Prefix | Non-Capturing Options                             |
|-----------------------|-------:|:--------------------------------------------------|
| i-Family (Apple)      |    `i` | `(?:Phone\|Pad\|Pod\|Mac\|Message\|Cloud\|Tunes)` |
| e-Family (electronic) |    `e` | `(?:Mail\|Book\|Pub\|Commerce)`                   |
| x-Family              |    `x` | `(?:86\|64\|AI\|Unit)`                            |
"""


ACRONYM_RXS: Final[str] = r"[A-Z\d]{2,}(v?\.?\d+)?"
ANY_CASE_WORD_RXS: Final[str] = r"[a-zA-Z0-9]+"
CAPITALIZED_WORD_RXS: Final[str] = r"[A-Z][a-z0-9]*"
LOWER_CASE_WORD_RXS: Final[str] = r"[a-z0-9]+"
UPPER_CASE_WORD_RXS: Final[str] = r"[A-Z0-9]+"
UPPER_OR_LOWER_CASE_WORD_RXS: Final[str] = r"[a-zA-Z0-9]+"

CAMEL_CASE_RGX: Final[Pattern] = compile(rf""^{LOWER_CASE_WORD_RXS}({CAPITALIZED_WORD_RXS})*$")
CONSTANT_CASE_RGX: Final[Pattern] = compile(rf"^{UPPER_CASE_WORD_RXS}(_{UPPER_CASE_WORD_RXS})*$")
#DOT_CASE_RGX: Final[Pattern] = compile(
#KEBAB_CASE_RGX: Final[Pattern] = compile(
#LNX_PATH_CASE_RGX: Final[Pattern] = compile(
#LOWER_CASE_RGX: Final[Pattern] = compile(
#PASCAL_CASE_RGX: Final[Pattern] = compile(

########## Enumerations ##########

class StrCase(IntEnum):
    """
    Enumeration for string case types.
    """
    CAMEL       = 1
    CONSTANT    = 2
    DOT         = 3
    KEBAB       = 4
    LNX_PATH    = 5
    LOWER       = 6
    PASCAL      = 7
    SENTENCE    = 8
    SNAKE       = 9
    SPACE       = 10
    TITLE       = 11
    UPPER       = 12
    WIN_PATH    = 13
    
########## Functions ##########

def is_camel_case(value: str) -> bool:
    """
    Check if a string is in camel case.
    
    Args:
        value (str): The string to check.
        
    Returns:
        bool: True if the string is in camel case, False otherwise.
    """
    camel_case_rgx: Pattern = compile(r"^[a-z]+([A-Z][a-z]*)*$")
    
    return value == to_case(value, StrCase.CAMEL)

def to_case(value: str, case: StrCase) -> str:
    """
    Convert a string to the specified case.
    
    Args:
        value (str): The string to convert.
        case (StrCase): The case to convert to.
        
    Returns:
        str: The converted string.
    """
    # Switch
    match case:
        case StrCase.CAMEL:
            return casefy.camelcase(value)
        case StrCase.CONSTANT:
            return casefy.constcase(value)
        case StrCase.DOT:
            return casefy.dotcase(value)
        case StrCase.KEBAB:
            return casefy.kebabcase(value)
        case StrCase.LNX_PATH:
            return casefy.separatorcase(value, sep="/")
        case StrCase.LOWER:
            return casefy.lowercase(value)
        case StrCase.PASCAL:
            return casefy.pascalcase(value)
        case StrCase.SENTENCE:
            return casefy.sentencecase(value)
        case StrCase.SNAKE:
            return casefy.snakecase(value)
        case StrCase.SPACE:
            return casefy.separatorcase(value, sep=" ")
        case StrCase.TITLE:
            return casefy.titlecase(value)
        case StrCase.UPPER:
            return casefy.uppercase(value)
        case StrCase.WIN_PATH:
            return casefy.separatorcase(value, sep="\\")
        case _:
            raise ValueError(f"Unimplemented case: {case}")

