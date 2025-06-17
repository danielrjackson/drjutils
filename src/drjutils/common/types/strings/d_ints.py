"""
# Daniel's Type Utilities

This module provides utilities for working with basic types (and strings that represent them).
This is mostly intended to be used with configuration files.

Copyright 2025 Daniel Robert Jackson

### Constants:

| Constant       | Type         | Description                            |
|----------------|--------------|----------------------------------------|
| `INF`          | `float`      | Infinity                               |
| `NEG_INF`      | `float`      | Negative Infinity                      |
| `NAN`          | `float`      | Not a Number                           |
| `BOOL_RGX`     | `re.Pattern` | Boolean Regex                          |
| `BOOL_RXS`     | `str`        | Boolean Regex String                   |
| `COMPLEX_RGX`  | `re.Pattern` | Complex Number Regex                   |
| `COMPLEX_RXS`  | `str`        | Complex Number Regex String            |
| `FRACTION_RGX` | `re.Pattern` | Fraction Regex                         |
| `FRACTION_RXS` | `str`        | Fraction Regex String                  |
| `INT_RGX`      | `re.Pattern` | Integer Regex                          |
| `INT_RXS`      | `str`        | Integer Regex String                   |
| `INT_DEC_RGX`  | `re.Pattern` | Decimal (Base-10) Integer Regex        |
| `INT_DEC_RXS`  | `str`        | Decimal (Base-10) Integer Regex String |
| `INT_BIN_RGX`  | `re.Pattern` | Binary Integer Regex                   |
| `INT_BIN_RXS`  | `str`        | Binary Integer Regex String            |
| `INT_HEX_RGX`  | `re.Pattern` | Hexadecimal Integer Regex              |
| `INT_HEX_RXS`  | `str`        | Hexadecimal Integer Regex String       |
| `INT_OCT_RGX`  | `re.Pattern` | Octal Integer Regex                    |
| `INT_OCT_RXS`  | `str`        | Octal Integer Regex String             |
| `REAL_RGX`     | `re.Pattern` | Real Regex                             |
| `REAL_RXS`     | `str`        | Real Regex String                      |
| `REAL_BSC_RGX` | `re.Pattern` | Basic Real Regex                       |
| `REAL_BSC_RXS` | `str`        | Basic Real Regex String                |
| `REAL_SCI_RGX` | `re.Pattern` | Scientific Notation Real Regex         |
| `REAL_SCI_RXS` | `str`        | Scientific Notation Real Regex String  |
| `NUM_RGX`      | `re.Pattern` | Number Regex                           |
| `NUM_RXS`      | `str`        | Number Regex String                    |

### Functions:

| Function             | Description                                                   |
|----------------------|---------------------------------------------------------------|
| `check_bool`         | Check if a value represents a boolean                         |
| `check_complex`      | Check if a value represents a complex number                  |
| `check_fraction`     | Check if a value represents a fraction                        |
| `check_int`          | Check if a value represents an integer                        |
| `check_int_dec`      | Check if a string represents a decimal (base-10) integer      |
| `check_int_bin`      | Check if a string represents a binary integer                 |
| `check_int_hex`      | Check if a string represents a hexadecimal integer            |
| `check_int_oct`      | Check if a string represents an octal integer                 |
| `check_real`         | Check if a value represents a float                           |
| `check_real_basic`   | Check if a string represents a basic float                    |
| `check_real_scinot`  | Check if a string represents in scientific notation           |
| `check_number`       | Check if a value represents a number of any type              |
| `is_bool`            | Indicate if a value represents a boolean                      |
| `is_complex`         | Indicate if a value represents a complex number               |
| `is_fraction`        | Indicate if a value represents a fraction                     |
| `is_int`             | Indicate if a value represents an integer                     |
| `is_int_dec`         | Indicate if a string represents a decimal (base-10) integer   |
| `is_int_bin`         | Indicate if a string represents a binary integer              |
| `is_int_hex`         | Indicate if a string represents a hexadecimal integer         |
| `is_int_oct`         | Indicate if a string represents an octal integer              |
| `is_real`            | Indicate if a value represents a float                        |
| `is_real_basic`      | Indicate if a string represents a basic float                 |
| `is_real_scinot`     | Indicate if a string represents in scientific notation        |
| `is_number`          | Indicate if a string represents a number of any type          |
| `to_number`          | Convert a string to a number of the appropriate type          |
| `to_bool_str`        | Create a string toted_str as a boolean                        |
| `to_complex_str`     | Create a string toted_str as a complex number                 |
| `to_fraction_str`    | Create a string toted_str as a fraction                       |
| `to_int_str`         | Create a string toted_str as an integer                       |
| `to_int_bin_str`     | Create a string toted_str as a binary integer                 |
| `to_int_hex_str`     | Create a string toted_str as a hexadecimal integer            |
| `to_int_oct_str`     | Create a string toted_str as an octal integer                 |
| `to_real_str`        | Create a string toted_str as a real (float) number            |
| `to_real_basic_str`  | Create a string toted_str as a basic real number (not scinot) |
| `to_real_scinot_str` | Create a string toted_str in scientific notation              |
| `to_number_str`      | Create a string toted_str appropriately for the type          |
"""

"""
Standard Libraries
"""
from numbers import Complex, Fraction, Integral, Real
from re import compile, IGNORECASE
from typing import Final, Pattern, Union

__all__ = [
    # Constants #
    "INF",                  # Infinity
    "NEG_INF",              # Negative Infinity
    "NAN",                  # Not a Number
    "BOOL_RGX",             # Boolean Regex
    "BOOL_RXS",             # Boolean Regex String
    "COMPLEX_RGX",          # Complex Number Regex
    "COMPLEX_RXS",          # Complex Number Regex String
    "FRACTION_RGX",         # Fraction Regex
    "FRACTION_RXS",         # Fraction Regex String
    "INT_RGX",              # Integer Regex
    "INT_RXS",              # Integer Regex String
    "INT_DEC_RGX",          # Decimal (Base-10) Integer Regex
    "INT_DEC_RXS",          # Decimal (Base-10) Integer Regex String
    "INT_BIN_RGX",          # Binary Integer Regex
    "INT_BIN_RXS",          # Binary Integer Regex String
    "INT_HEX_RGX",          # Hexadecimal Integer Regex
    "INT_HEX_RXS",          # Hexadecimal Integer Regex String
    "INT_OCT_RGX",          # Octal Integer Regex
    "INT_OCT_RXS",          # Octal Integer Regex String
    "REAL_RGX",             # Real Regex
    "REAL_RXS",             # Real Regex String
    "REAL_BSC_RGX",         # Basic Real Regex
    "REAL_BSC_RXS",         # Basic Real Regex String
    "REAL_SCI_RGX",         # Scientific Notation Real Regex
    "REAL_SCI_RXS",         # Scientific Notation Real Regex String
    "NUM_RGX",              # Number Regex
    "NUM_RXS",              # Number Regex String
    # Functions #
    "check_bool",           # Check that the value represents a boolean
    "check_complex",        # Check that the value represents a complex number
    "check_fraction",       # Check that the value represents a fraction
    "check_int",            # Check that the value represents an integer (any valid integer format)
    "check_int_dec",        # Check that the string represents a decimal (base-10) integer
    "check_int_bin",        # Check that the string represents a binary integer
    "check_int_hex",        # Check that the string represents a hexadecimal integer
    "check_int_oct",        # Check that the string represents an octal integer
    "check_real",           # Check that the value represents a float (any valid real format)
    "check_real_basic",     # Check that the string represents a basic real number (not scinot)
    "check_real_scinot",    # Check that the string represents a real number in scientific notation
    "check_number",         # Check that the value represents a number of any type
    "is_bool",              # Indicate if the value represents a boolean
    "is_complex",           # Indicate if the value represents a complex number
    "is_fraction",          # Indicate if the value represents a fraction
    "is_int",               # Indicate if the value represents an integer (any valid integer format)
    "is_int_dec",           # Indicate if the string represents a decimal (base-10) integer
    "is_int_bin",           # Indicate if the string represents a binary integer
    "is_int_hex",           # Indicate if the string represents a hexadecimal integer
    "is_int_oct",           # Indicate if the string represents an octal integer
    "is_real",              # Indicate if the value represents a float (any valid real format)
    "is_real_basic",        # Indicate if the string represents a basic real number (not scinot)
    "is_real_scinot",       # Indicate if the string represents a real number in scientific notation
    "is_number",            # Indicate if the value represents a number of any type
    "to_number",            # Convert to a number of the appropriate type
    "to_bool_str",          # Create a string toted_str as a boolean
    "to_complex_str",       # Create a string toted_str as a complex number
    "to_fraction_str",      # Create a string toted_str as a fraction
    "to_int_str",           # Create a string toted_str as an integer
    "to_int_bin_str",       # Create a string toted_str as a binary integer
    "to_int_hex_str",       # Create a string toted_str as a hexadecimal integer
    "to_int_oct_str",       # Create a string toted_str as an octal integer
    "to_real_str",          # Create a string toted_str as a real (float) number
    "to_real_basic_str",    # Create a string toted_str as a basic real number (not scinot)
    "to_real_scinot_str",   # Create a string toted_str in scientific notation
    "to_number_str"         # Create a string toted_str appropriately for the type of number
]

########## Constants ##########

INF:        Final[float] = float("inf")
"""### Infinity"""

NEG_INF:    Final[float] = float("-inf")
"""### Negative Infinity"""

NAN:        Final[float] = float("nan")
"""### Not a Number"""

### Sign Indicator Regexes ###

SIGN_RXS: Final[str] = r"[+-]"
"""
### Sign Regex String

*   values: `+` or `-`
*   Usage: `re.compile(SIGN_RXS)`

### Pattern: `[+-]`

See also: `SIGN_OPT_RXS`
"""

SIGN_OPT_RXS: Final[str] = r"[+-]?"
"""
### Optional Sign Regex String

*   values: `+`, `-`, or empty string
*   Usage: `re.compile(SIGN_OPT_RXS)`

### Pattern: `[+-]?`

See also: `SIGN_RXS`
"""

### Integer Regexes ###

## Decimal Integer Regexes ##

INT_DEC_MAG_RXS: Final[str] = r"\d+"
r"""
### Unsigned Decimal Integer (Base-10) Digits Regex String

*   e.g.: `0`, `1`, `23`, `456`, `5678`, `0123456789`, etc.
*   Usage: `re.compile(INT_DEC_MAG_RXS)`

### Pattern: `\d+`

See also:
    *   `INT_DEC_RXS`, `INT_DEC_RGX`
    *   `INT_MAG_RXS`
    *   `INT_RXS`, `INT_RGX`
"""

INT_DEC_RXS: Final[str] = f"{SIGN_OPT_RXS}{INT_DEC_MAG_RXS}"
r"""
### Signed Decimal Integer (Base-10) Regex String

*   e.g.: `0`, `+0`, `-0`, `1`, `+2`, `-3`, `45`, `+678`, `-0123456789`, etc.
*   Usage: `re.compile(INT_DEC_RXS)`

### Pattern: `[+-]?\d+`

#### Signed Decimal Integer Regex Structure:

|   Sign? | Digits |
|--------:|:-------|
| `[+-]?` | `\d+`  |

See also:
    *   `INT_DEC_MAG_RXS`
    *   `INT_DEC_RGX`
    *   `INT_RXS`, `INT_RGX`
"""

INT_DEC_RGX: Final[Pattern] = compile(rf"^\s*{INT_DEC_RXS}\s*$")
r"""
### Signed Decimal Integer (Base-10) Regex

*   e.g.: `0`, `+0`, `-0`, `1`, `+2`, `-3`, `45`, `+678`, `-0123456789`, etc.
*   Usage: INT_DEC_RGX.match("0")

### Pattern: `^\s*[+-]?\d+\s*$`

#### Signed Decimal Integer Regex Structure:

| Prefix? |  Sign?  | Digits | Suffix? |
|--------:|:-------:|:-------|:--------|
|  `^\s*` | `[+-]?` | `\d+`  | `\s*$`  |

See also:
    *   `INT_DEC_RXS`
    *   `INT_RXS`, `INT_RGX`
"""

## Binary Integer Regexes ##

INT_BIN_MAG_DGT_RXS: Final[str] = r"[01]+"
"""
### Unsigned Binary Integer Digits Regex String

*   e.g.: `0`, `1`, `10`, `11`, `1010`, `1101`, `1110`, etc.
*   Usage: `re.compile(INT_BIN_MAG_DGT_RXS)`

### Pattern: `[01]+`

See also:
    *   `INT_BIN_MAG_RXS`
    *   `INT_BIN_RXS`, `INT_BIN_RGX`
    *   `INT_NON_DEC_MAG_RXS`
    *   `INT_NON_DEC_RXS`, `INT_NON_DEC_RGX`
    *   `INT_MAG_RXS`
    *   `INT_RXS`, `INT_RGX`
"""

INT_BIN_MAG_RXS: Final[str] = f"0b{INT_BIN_MAG_DGT_RXS}"
"""
### Unsigned Binary Integer Regex String

*   e.g.: `0b0`, `0B1`, `0dec`, `0B11`, `0dec10`, `0B11010110`, etc.
*   Usage: `re.compile(INT_BIN_MAG_RXS, flags=re.IGNORECASE)`

### Pattern: `0b[01]+`

#### Unsigned Binary Integer Regex Structure:

| Base | Digits  |
|-----:|:--------|
| `0b` | `[01]+` |

See also:
    *   `INT_BIN_MAG_DGT_RXS`
    *   `INT_BIN_RXS`, `INT_BIN_RGX`
    *   `INT_NON_DEC_MAG_RXS`
    *   `INT_NON_DEC_RXS`, `INT_NON_DEC_RGX`
    *   `INT_MAG_RXS`
    *   `INT_RXS`, `INT_RGX`
"""

INT_BIN_RXS: Final[str] = f"{SIGN_OPT_RXS}{INT_BIN_MAG_RXS}"
"""
### Signed Binary Integer Regex String

*   e.g.: `0b0`, `+0B0`, `-0b0`, `0B1`, `+0dec`, `-0B1011`, `0b11010110`, etc.
*   Usage: `re.compile(INT_BIN_RXS, flags=re.IGNORECASE)`

### Pattern: `[+-]?0b[01]+`

#### Signed Binary Integer Regex Structure:

|   Sign? | Base | Digits  |
|--------:|:----:|:--------|
| `[+-]?` | `0b` | `[01]+` |

See also:
    *   `INT_BIN_MAG_RXS`
    *   `INT_BIN_RGX`
    *   `INT_NON_DEC_RXS`, `INT_NON_DEC_RGX`
    *   `INT_RXS`, `INT_RGX`
"""

INT_BIN_RGX: Final[Pattern] = compile(rf"^\s*{INT_BIN_RXS}\s*$", flags=IGNORECASE)
r"""
### Signed Binary Integer Regex Pattern

*   e.g.: `0b0`, `+0B0`, `-0b0`, `0B1`, `+0dec`, `-0B1011`, `0b11010110`, etc.
*   Usage: INT_BIN_RGX.match("0dec10")

### Pattern: `^\s*[+-]?0b[01]+\s*$`

#### Signed Binary Integer Regex Structure:

| Prefix? |  Sign?  | Base |  Digits | Suffix? |
|--------:|:-------:|:----:|:-------:|:--------|
|  `^\s*` | `[+-]?` | `0b` | `[01]+` | `\s*$`  |

See also:
    *   `INT_BIN_RXS`
    *   `INT_NON_DEC_RXS`, `INT_NON_DEC_RGX`
    *   `INT_RXS`, `INT_RGX`
"""

## Hexadecimal Integer Regexes ##

INT_HEX_MAG_DGT_RXS: Final[str] = r"[\da-f]+"
r"""
### Unsigned Hexadecimal Integer Digits Regex String

*   e.g.: `0`, `1`, `A`, `f`, `20`, `3B4C`, `5d6E7F89`, etc.
*   Usage: `re.compile(INT_HEX_MAG_DGT_RXS, flags=re.IGNORECASE)`

### Pattern: `[\da-f]+`

See also:
    *   `INT_HEX_MAG_RXS`
    *   `INT_HEX_RXS`, `INT_HEX_RGX`
    *   `INT_NON_DEC_MAG_RXS`
    *   `INT_NON_DEC_RXS`, `INT_NON_DEC_RGX`
    *   `INT_MAG_RXS`
    *   `INT_RXS`, `INT_RGX`
"""

INT_HEX_MAG_RXS: Final[str] = f"0x{INT_HEX_MAG_DGT_RXS}"
r"""
### Unsigned Hexadecimal Integer Regex String

*   e.g.: `0x0`, `0X1`, `0xA`, `0Xf`, `0x20`, `0X3B4C`, `0x5d6E7F89`, etc.
*   Usage: `re.compile(INT_HEX_MAG_RXS, flags=re.IGNORECASE)`

### Pattern: `0x[\da-f]+`

##### Unsigned Hexadecimal Integer Regex Structure:

| Base | Digits     |
|-----:|:-----------|
| `0x` | `[\da-f]+` |

See also:
    *   `INT_HEX_MAG_DGT_RXS`
    *   `INT_HEX_RXS`, `INT_HEX_RGX`
    *   `INT_NON_DEC_MAG_RXS`
    *   `INT_NON_DEC_RXS`, `INT_NON_DEC_RGX`
    *   `INT_MAG_RXS`
    *   `INT_RXS`, `INT_RGX`
"""

INT_HEX_RXS: Final[str] = f"{SIGN_OPT_RXS}{INT_HEX_MAG_RXS}"
r"""
### Signed Hexadecimal Integer Regex String

*   e.g.: `0x0`, `+0X0`, `-0x0`, `0X1`, `+0xA`, `-0Xf`, `0x20`, `+0X3B4C`, `-0x5d6E7F89`, etc.
*   Usage: `re.compile(INT_HEX_RXS, flags=re.IGNORECASE)`

### Pattern: `[+-]?0x[\da-f]+`

#### Signed Hexadecimal Integer Regex Structure:

|   Sign? | Base |  Digits    |
|--------:|:----:|:-----------|
| `[+-]?` | `0x` | `[\da-f]+` |

See also:
    *   `INT_HEX_MAG_RXS`
    *   `INT_HEX_RGX`
    *   `INT_NON_DEC_RXS`, `INT_NON_DEC_RGX`
    *   `INT_RXS`, `INT_RGX`
"""

INT_HEX_RGX: Final[Pattern] = compile(rf"^\s*{INT_HEX_RXS}\s*$", flags=IGNORECASE)
r"""
### Signed Hexadecimal Integer Regex Pattern

*   e.g.: `0x0`, `+0X0`, `-0x0`, `0X1`, `+0xA`, `-0Xf`, `0x20`, `+0X3B4C`, `-0x5d6E7F89`, etc.
*   Usage: INT_HEX_RGX.match("0x20")

### Pattern: `^\s*[+-]?0x[\da-f]+\s*$`

#### Signed Hexadecimal Integer Regex Structure:

| Prefix? |  Sign?  | Base |   Digits   | Suffix? |
|--------:|:-------:|:----:|:----------:|:--------|
|  `^\s*` | `[+-]?` | `0x` | `[\da-f]+` | `\s*$`  |

See also:
    *   `INT_HEX_RXS`
    *   `INT_NON_DEC_RXS`, `INT_NON_DEC_RGX`
    *   `INT_RXS`, `INT_RGX`
"""

## Octal Integer Regexes ##

INT_OCT_MAG_DGT_RXS: Final[str] = r"[0-7]+"
"""
### Unsigned Octal Integer Digits Regex String

*   e.g.: `0`, `1`, `7`, `23`, `4567`, `01234567`, etc.
*   Usage: `re.compile(INT_OCT_MAG_DGT_RXS)`

### Pattern: `[0-7]+`

See also:
    *   `INT_OCT_MAG_RXS`
    *   `INT_OCT_RXS`, `INT_OCT_RGX`
    *   `INT_NON_DEC_MAG_RXS`,
    *   `INT_NON_DEC_RXS`, `INT_NON_DEC_RGX`
    *   `INT_MAG_RXS`
    *   `INT_RXS`, `INT_RGX`
"""

INT_OCT_MAG_RXS: Final[str] = rf"0o{INT_OCT_MAG_DGT_RXS}"
"""
### Unsigned Octal Integer Regex String

*   e.g.: `0o0`, `0O1`, `0o7`, `0O23`, `0o4567`, `0O01234567`, etc.
*   Usage: `re.compile(INT_OCT_MAG_RXS, flags=re.IGNORECASE)`

### Pattern: `0o[0-7]+`

#### Unsigned Octal Digits Regex Structure:

| Base | Digits   |
|-----:|:---------|
| `0o` | `[0-7]+` |

See also:
    *   `INT_OCT_MAG_DGT_RXS`
    *   `INT_OCT_RXS`, `INT_OCT_RGX`
    *   `INT_NON_DEC_MAG_RXS`
    *   `INT_NON_DEC_RXS`, `INT_NON_DEC_RGX`
    *   `INT_MAG_RXS`
    *   `INT_RXS`, `INT_RGX`
"""

INT_OCT_RXS: Final[str] = f"{SIGN_OPT_RXS}{INT_OCT_MAG_RXS}"
"""
### Signed Octal Integer Regex String

*   e.g.: `0o0`, `+0O0`, `-0o0`, `0O1`, `+0o7`, `-0O23`, `0o4567`, `+0O01234567`, etc.
*   Usage: `re.compile(INT_OCT_RXS, flags=re.IGNORECASE)`

### Pattern: `[+-]?0o[0-7]+`

#### Signed Octal Integer Regex Structure:

|   Sign? | Base | Digits   |
|--------:|:----:|:---------|
| `[+-]?` | `0o` | `[0-7]+` |

See also:
    *   `INT_OCT_MAG_RXS`
    *   `INT_OCT_RGX`
    *   `INT_NON_DEC_RXS`, `INT_NON_DEC_RGX`
    *   `INT_RXS`, `INT_RGX`
"""

INT_OCT_RGX: Final[Pattern] = compile(rf"^\s*{INT_OCT_RXS}\s*$", flags=IGNORECASE)
r"""
### Signed Octal Integer Regex Pattern

*   e.g.: `0o0`, `+0O0`, `-0o0`, `0O1`, `+0o7`, `-0O23`, `0o4567`, `+0O01234567`, etc.
*   Usage: INT_OCT_RGX.match("0o4567")

### Pattern: `^\s*[+-]?0o[0-7]+\s*$`

#### Signed Octal Integer Regex Structure:

| Prefix? |  Sign?  | Base |  Digits  | Suffix? |
|--------:|:-------:|:----:|:--------:|:--------|
|  `^\s*` | `[+-]?` | `0o` | `[0-7]+` | `\s*$`  |

See also:
    *   `INT_OCT_RXS`
    *   `INT_NON_DEC_RXS`, `INT_NON_DEC_RGX`
    *   `INT_RXS`, `INT_RGX`
"""

## Non-Decimal Integer Regexes (Hex, Bin, Oct) ##

INT_NON_DEC_MAG_RXS: Final[str] = rf"{INT_BIN_MAG_RXS}|{INT_HEX_MAG_RXS}|{INT_OCT_MAG_RXS}"
r"""
### Unsigned Non-Decimal Integer Magnitude Regex String

*   Supports Hexadecimal, Binary, and Octal Integers
*   Hexadecimal:
    *   `0x` followed by hexadecimal digits (`0-9`, `a-f`)
    *   e.g.: `0x1a`, `0X2F`, `0x3B`, etc.
*   Binary:
    *   `0b` followed by binary digits (`0-1`)
    *   e.g.: `0dec10`, `0B1101`, `0b1110`, etc.
*   Octal:
    *   `0o` followed by octal digits (`0-7`)
    *   e.g.: `0o123`, `0O4567`, `0o01234567`, etc.
*   Usage: `re.compile(INT_NON_DEC_MAG_RXS, flags=re.IGNORECASE)`

### Pattern: `0x[\da-f]+|0b[01]+|0o[0-7]+`

#### Numerical Base Option Series: `...|...`
 | Option | Base | Prefix | Digits     |
 |-------:|:----:|-------:|:-----------|
 |      1 |  Hex |   `0x` | `[\da-f]+` |
 |      2 |  Bin |   `0b` | `[01]+`    |
 |      3 |  Oct |   `0o` | `[0-7]+`   |
 
 See also:
    *   `INT_BIN_MAG_RXS`
    *   `INT_HEX_MAG_RXS`
    *   `INT_OCT_MAG_RXS`
    *   `INT_NON_DEC_RXS`, `INT_NON_DEC_RGX`
    *   `INT_MAG_RXS`
    *   `INT_RXS`, `INT_RGX`
"""

INT_NON_DEC_RXS: Final[str] = f"{SIGN_OPT_RXS}(?:{INT_NON_DEC_MAG_RXS})"
r"""
### Signed Non-Decimal Integer Regex String

*   Supports Hexadecimal, Binary, and Octal Integers
*   Hexadecimal:
    *   `0x` followed by hexadecimal digits (`0-9`, `a-f`)
    *   e.g.: `0x1a`, `0X2F`, `0x3B`, etc.
*   Binary:
    *   `0b` followed by binary digits (`0-1`)
    *   e.g.: `0dec10`, `0B1101`, `0b1110`, etc.
*   Octal:
    *   `0o` followed by octal digits (`0-7`)
    *   e.g.: `0o123`, `0O4567`, `0o01234567`, etc.
*   Usage: `re.compile(INT_NON_DEC_RXS, flags=re.IGNORECASE)`

### Pattern: `[+-]?(?:0x[\da-f]+|0b[01]+|0o[0-7]+)`

#### Signed Non-Decimal Integer Regex Structure:

|   Sign? | Options        |
|--------:|:---------------|
| `[+-]?` | `(?:...\|...)` |

#### Non-Decimal Integer Non-Capturing Option Group: `(?:...|...)`

| Option | Base | Prefix | Digits     |
|-------:|:----:|-------:|:-----------|
|      1 |  Hex |   `0x` | `[\da-f]+` |
|      2 |  Bin |   `0b` | `[01]+`    |
|      3 |  Oct |   `0o` | `[0-7]+`   |

See also:
    *   `INT_NON_DEC_MAG_RXS`
    *   `INT_NON_DEC_RGX`
    *   `INT_RXS`, `INT_RGX`
"""

INT_NON_DEC_RGX: Final[Pattern] = compile(rf"^\s*{INT_NON_DEC_RXS}\s*$", flags=IGNORECASE)
r"""
### Signed Non-Decimal Integer Regex String

*   Supports Hexadecimal, Binary, and Octal Integers
*   Hexadecimal:
    *   `0x` followed by hexadecimal digits (`0-9`, `a-f`)
    *   e.g.: `0x1a`, `0X2F`, `0x3B`, etc.
*   Binary:
    *   `0b` followed by binary digits (`0-1`)
    *   e.g.: `0dec10`, `0B1101`, `0b1110`, etc.
*   Octal:
    *   `0o` followed by octal digits (`0-7`)
    *   e.g.: `0o123`, `0O4567`, `0o01234567`, etc.
*   Usage: INT_NON_DEC_RGX.match("0x1a")

### Pattern: `^\s*[+-]?(?:0x[\da-f]+|0b[01]+|0o[0-7]+)\s*$`

#### Signed Non-Decimal Integer Regex Structure:

| Prefix? |   Sign?  |     Options    | Suffix? |
|--------:|:--------:|:--------------:|:--------|
|  `^\s*` | `[+-]?`  | `(?:...\|...)` | `\s*$`  |

#### Non-Decimal Integer Non-Capturing Option Group: `(?:...|...)`

| Option | Base | Prefix | Digits     |
|-------:|:----:|-------:|:-----------|
|      1 |  Hex |   `0x` | `[\da-f]+` |
|      2 |  Bin |   `0b` | `[01]+`    |
|      3 |  Oct |   `0o` | `[0-7]+`   |

See also:
    *   `INT_NON_DEC_RXS`
    *   `INT_RXS`, `INT_RGX`
"""

## Integer Regex String ##

INT_MAG_RXS: Final[str] = rf"{INT_DEC_MAG_RXS}|{INT_NON_DEC_MAG_RXS}"
r"""
### Unsigned Integer Regex String

*   Supports Decimal, Hexadecimal, Binary, and Octal Integers
*   Decimal:
    *   e.g.: `0`, `1`, `23`, `456`, `5678`, `0123456789`, etc.
*   Hexadecimal:
    *   e.g.: `0x1a`, `0X2F`, `0x3b`, etc.
*   Binary:
    *   e.g.: `0dec10`, `0B1101`, `0b1110`, etc.
*   Octal:
    *   e.g.: `0o123`, `0O4567`, `0o01234567`, etc.
*   Usage: `re.compile(INT_MAG_RXS, flags=re.IGNORECASE)`

### Pattern: `\d+|0x[\da-f]+|0b[01]+|0o[0-7]+`

#### Integer Option Series: `...|...`

| Option | Base | Prefix | Digits     | Description         |
|-------:|-----:|-------:|:-----------|:--------------------|
|      1 |  Dec |        | `\d+`      | Decimal Integer     |
|      2 |  Hex |   `0x` | `[\da-f]+` | Hexadecimal Integer |
|      3 |  Bin |   `0b` | `[01]+`    | Binary Integer      |
|      4 |  Oct |   `0o` | `[0-7]+`   | Octal Integer       |

See also:
    *   `INT_DEC_MAG_RXS`
    *   `INT_NON_DEC_MAG_RXS`
    *   `INT_RXS`, `INT_RGX`
"""

INT_RXS: Final[str] = f"{SIGN_OPT_RXS}(?:{INT_MAG_RXS})"
r"""
### Signed Integer Regex String

*   Supports Decimal, Hexadecimal, Binary, and Octal Integers
*   Decimal:
    *   e.g.: `0`, `+0`, `-0`, `1`, `+2`, `-3`, `45`, `+678`, `-0123456789`, etc.
*   Hexadecimal:
    *   e.g.: `0x0`, `+0X0`, `-0x0`, `0X1`, `+0xA`, `-0Xf`, `0x20`, `+0X3B4C`, `-0x5d6E7F89`, etc.
*   Binary:
    *   e.g.: `0b0`, `+0B0`, `-0b0`, `0B1`, `+0dec`, `-0B1011`, `0b11010110`, etc.
*   Octal:
    *   e.g.: `0o0`, `+0O0`, `-0o0`, `0O1`, `+0o7`, `-0O23`, `0o4567`, `+0O01234567`, etc.
*   Usage: `re.compile(INT_RXS, flags=re.IGNORECASE)`

### Pattern: `[+-]?(?:\d+|0x[\da-f]+|0b[01]+|0o[0-7]+)`

#### Signed Integer Regex Structure:
|   Sign? | Options        |
|--------:|:---------------|
| `[+-]?` | `(?:...\|...)` |

#### Integer Non-Capturing Option Group: `(?:...|...)`

| Option | Base | Prefix | Digits     | Description         |
|-------:|-----:|-------:|:-----------|:--------------------|
|      1 |  Dec |        | `\d+`      | Decimal Integer     |
|      2 |  Hex |   `0x` | `[\da-f]+` | Hexadecimal Integer |
|      3 |  Bin |   `0b` | `[01]+`    | Binary Integer      |
|      4 |  Oct |   `0o` | `[0-7]+`   | Octal Integer       |

See also:
    *   `INT_MAG_RXS`
    *   `INT_RGX
"""

INT_RGX: Final[Pattern] = compile(rf"^\s*{INT_RXS}\s*$", flags=IGNORECASE)
r"""
### Signed Integer Regex Pattern

*   Supports Decimal, Hexadecimal, Binary, and Octal Integers
*   Decimal:
    *   e.g.: `0`, `+0`, `-0`, `1`, `+2`, `-3`, `45`, `+678`, `-0123456789`, etc.
*   Hexadecimal:
    *   e.g.: `0x0`, `+0X0`, `-0x0`, `0X1`, `+0xA`, `-0Xf`, `0x20`, `+0X3B4C`, `-0x5d6E7F89`, etc.
*   Binary:
    *   e.g.: `0b0`, `+0B0`, `-0b0`, `0B1`, `+0dec`, `-0B1011`, `0b11010110`, etc.
*   Octal:
    *   e.g.: `0o0`, `+0O0`, `-0o0`, `0O1`, `+0o7`, `-0O23`, `0o4567`, `+0O01234567`, etc.
*   Usage: INT_RGX.match("0x1a")

### Pattern: `^\s*[+-]?(?:\d+|0x[\da-f]+|0b[01]+|0o[0-7]+)\s*$`

#### Signed Integer Regex Structure:

| Prefix? |   Sign?  |     Options    | Suffix? |
|--------:|:--------:|:--------------:|:--------|
|  `^\s*` | `[+-]?`  | `(?:...\|...)` | `\s*$`  |

#### Integer Non-Capturing Option Group: `(?:...|...)`

| Option | Base | Prefix | Digits     | Description         |
|-------:|-----:|-------:|:-----------|:--------------------|
|      1 |  Dec |        | `\d+`      | Decimal Integer     |
|      2 |  Hex |   `0x` | `[\da-f]+` | Hexadecimal Integer |
|      3 |  Bin |   `0b` | `[01]+`    | Binary Integer      |
|      4 |  Oct |   `0o` | `[0-7]+`   | Octal Integer       |

See also: `INT_RXS`
"""

### Real Number Regexes ###

REAL_MAG_DGT_RXS: Final[str] = r"\d+\.\d*|\.\d+"
r"""
### Unsigned Real Digits Regex String

*   Supports Valid Unsigned Real Digit Formats
*   Not Integer, Complex, or Fraction
*   Does not support Scientific Notation
*   e.g.: `0.0`, `1.0`, `23.456`, `78.`, `.901`, etc.
*   Usage: `re.compile(REAL_MAG_DGT_RXS)`

### Pattern: `\d+\.\d*|\.\d+`

#### Real Number Magnitude Digits Option Series: `...|...`

| Option |    Regex   | Description            |
|-------:|------------|:-----------------------|
|      1 | `\d+\.\d*` | Trailing Zero Optional |
|      2 | `\.\d+`    | No Leading Zero        |

See also:
    *   `REAL_MAG_SCINOT_OPT_DGT_RXS`, `REAL_MAG_SCINOT_OPT_RGX`
    *   `REAL_MAG_SCINOT_RXS`, `REAL_MAG_SCINOT_RGX`
    *   `REAL_SCINOT_OPT_RXS`, `REAL_SCINOT_OPT_RGX`
"""

REAL_SCINOT_EXP_RXS: Final[str] = r"e[+-]?\d+"
r"""
### Scientific Notation Exponent Regex String

*   Supports Exponential Part of Scientific Notation Only
*   Scientific Notation:
    *   Exponent Indicator (`e`)
    *   Optional Sign (`+` or `-`)
    *   Integer Exponent Value
*   e.g.: `e0`, `e+0`, `e-0`, `e1`, `e+2`, `e-3`, `e456`, etc.
*   Usage: `re.compile(REAL_SCINOT_EXP_RXS, flags=re.IGNORECASE)`

### Pattern: `e[+-]?\d+`

#### Exponent Regex Structure:

| Exp Ind |  Sign?  | Integer |
|--------:|:-------:|---------|
| `e`     | `[+-]?` | `\d+`   |

See also:
    *   `REAL_MAG_DGT_RXS`
    *   `REAL_BSC_MAG_RXS`
"""

REAL_SPEC_RXS: Final[str] = r"inf(?:inity)?|nan"
r"""
### Special Real Regex String

*   Supports Special Real Value Formats Only
*   Values: `inf`, `infinity`, `nan`
*   Notes:
    *   Used to build other regex strings
    *   Compile this regex string with the `IGNORECASE` flag

### Pattern: `inf(?:inity)?|nan`

#### Special Real Values Option Series: `...|...`

| Option |      Regex      |  Body | Suffix? | Description  |
|-------:|-----------------|------:|:--------|:-------------|
|      1 | `inf(?:inity)?` | `inf` | `inity` | Infinity     |
|      2 | `nan`           | `nan` |         | Not a Number |

<small>\*: Optional Suffix is Non-Capturing</small>
"""

REAL_MAG_SCINOT_DGT_RXS: Final[str] = rf"(?:{REAL_MAG_DGT_RXS}|\d+){REAL_SCINOT_EXP_RXS}"
r"""
### Unsigned Scientific Notation Regex String

*   Supports All Valid Unsigned Real Scientific Notation Formats
*   Not Integer, Complex, or Fraction
*   Optional Exponent Sign (`+` or `-`)
*   Does not include special values (e.g. `inf`, `nan`)
*   e.g.: `0.0e0`, `1.2e+3`, `4.e-5`, `.6e7`, `89e+10`, etc.
*   Usage: `re.compile(REAL_MAG_SCINOT_RXS, flags=re.IGNORECASE)`

### Pattern: `(?:\d+\.\d*|\.\d+|\d+)e[+-]?\d+`

#### Unsigned Scientific Notation Regex Structure:

| Significand Opts | Exp Ind |  Sign?  | Integer |
|-----------------:|:-------:|:-------:|:--------|
|   `(?:...\|...)` |   `e`   | `[+-]?` | `\d+`   |

#### Significand Non-Capturing Option Group: `(?:...|...)`

| Option |    Regex   | Description            |
|-------:|------------|:-----------------------|
|      1 | `\d+\.\d*` | Trailing Zero Optional |
|      2 | `\.\d+`    | No Leading Zero        |
|      3 | `\d+`      | Integer                |

See also:
    *   `REAL_MAG_DGT_RXS`
    *   `REAL_SCINOT_EXP_RXS`
    *   `REAL_SCINOT_RXS`, `REAL_SCINOT_RGX`
"""

REAL_SCINOT_RXS: Final[str] = rf"{SIGN_OPT_RXS}(?:{REAL_MAG_SCINOT_DGT_RXS}|{REAL_SPEC_RXS})"
r"""
### Signed Scientific Notation Regex String

*   Supports All Valid Signed Real Scientific Notation Formats
*   Not Integer, Complex, or Fraction
*   Optional Exponent Sign (`+` or `-`)
*   Does not include special values (e.g. `inf`, `nan`)
*   e.g.:
    * `0.0`, `+0.0`, `-0.0`, `1.0`, `+23.456`, etc.
    * `0.0e0`, `+0.0e-0`, `-0.0e+0`, `1.0e+2`, `+23.456e-3`, etc.
    * `inf`, `-inf`, `infinity`, `-infinity`, `nan`
*   Usage: `re.compile(REAL_SCINOT_RXS, flags=re.IGNORECASE)`

### Pattern: `[+-]?(?:(?:\d+\.\d*|\.\d+|\d+)e[+-]?\d+|inf(?:inity)?|nan)`

#### Signed Scientific Notation Regex Structure:

|  Sign?  |  Sci Not Opts  |
|--------:|:---------------|
| `[+-]?` | `(?:...\|...)` |

#### Scientific Notation Non-Capturing Option Group: `(?:...|...)`

| Option |       Regex       | Body    | NC Suffix? | Description         |
|-------:|-------------------|--------:|:-----------|:--------------------|
|      1 | See Sci Not Table | Options | Exponent   | Scientific Notation |
|      2 | `inf(?:inity)?`   |   `inf` | `inity`    | Infinity            |
|      3 | `nan`             |   `nan` |            | Not a Number        |

#### Signed Scientific Notation Regex Structure:

| Significand Opts | Exp Ind |  Sign?  | Integer |
|:----------------:|:-------:|:-------:|:--------|
|  `(?:...\|...)`  |   `e`   | `[+-]?` | `\d+`   |

#### Significand Non-Capturing Option Group: `(?:...|...)`

| Option |    Regex   | Description            |
|-------:|------------|:-----------------------|
|      1 | `\d+\.\d*` | Trailing Zero Optional |
|      2 | `\.\d+`    | No Leading Zero        |
|      3 | `\d+`      | Integer                |

See also:
    *   `REAL_MAG_SCINOT_DGT_RXS`
    *   `REAL_SCINOT_RGX`
"""

REAL_SCINOT_RGX: Final[Pattern] = compile(rf"^\s*{REAL_SCINOT_RXS}\s*$", flags=IGNORECASE)
r"""
### Real Scientific Notation Regex Pattern

*   Supports All Valid Signed Real Scientific Notation Formats
*   Not Integer, Complex, or Fraction
*   Optional Exponent Sign (`+` or `-`)
*   Does not include special values (e.g. `inf`, `nan`)
*   e.g.: `0.0`, `+0.0`, `-0.0`, `1.0`, `+23.456`, `-7e+2`, `+1.0e-3`, etc.
*   Usage: `REAL_SCINOT_RGX.match("1.0e-3")`

### Pattern: `^\s*[+-]?(?:(?:\d+\.\d*|\.\d+|\d+)e[+-]?\d+|inf(?:inity)?|nan)\s*$`

#### Signed Scientific Notation Regex Structure:
| Prefix? |  Sign?  |  Sci Not Opts  | Suffix? |
|--------:|:-------:|:--------------:|:--------|
|  `^\s*` | `[+-]?` | `(?:...\|...)` | `\s*$`  |

#### Scientific Notation Non-Capturing Option Group: `(?:...|...)`

| Option |       Regex       | Body    | NC Suffix? | Description         |
|-------:|-------------------|--------:|:-----------|:--------------------|
|      1 | See Sci Not Table | Options | Exponent   | Scientific Notation |
|      2 | `inf(?:inity)?`   |   `inf` | `inity`    | Infinity            |
|      3 | `nan`             |   `nan` |            | Not a Number        |

#### Signed Scientific Notation Regex Structure:

| Significand Opts | Exp Ind |  Sign?  | Integer |
|:----------------:|:-------:|:-------:|:--------|
|  `(?:...\|...)`  |   `e`   | `[+-]?` | `\d+`   |

#### Significand Non-Capturing Option Group: `(?:...|...)`

| Option |    Regex   | Description            |
|-------:|------------|:-----------------------|
|      1 | `\d+\.\d*` | Trailing Zero Optional |
|      2 | `\.\d+`    | No Leading Zero        |
|      3 | `\d+`      | Integer                |

See also:
    *   `REAL_SCINOT_RXS`
"""

REAL_MAG_SCINOT_OPT_DGT_RXS: Final[str] = rf"(?:{REAL_MAG_DGT_RXS}|\d+(?=e))(?:{REAL_SCINOT_EXP_RXS})?"
r"""
### Unsigned Real Number Regex String (Optional Scientific Notation)

*   Supports All Valid Unsigned Real Formats
*   Not Integer, Complex, or Fraction
*   Supports Scientific Notation
    *   Integer Significand only allowed with Scientific Notation
    *   Optional Exponent Sign (`+` or `-`)
*   Does not include special values (e.g. `inf`, `nan`)
*   e.g.: `0.0`, `1.0`, `23.456`, `7e+2`, `1.0e-3`, etc.
*   Usage: `re.compile(REAL_SCINOT_OPT_RXS)`

### Pattern: `(?:\d+\.\d*|\.\d+|\d+(?=e))(?:e[+-]?\d+)?`

#### Unsigned Real Number Regex Structure:

| Significand Opts | Sci Not?   |
|-----------------:|:-----------|
|   `(?:...\|...)` | `(?:...)?` |

#### Significand Non-Capturing Option Group: `(?:...|...)`

| Option |    Regex   | Description                            |
|-------:|------------|:---------------------------------------|
|      1 | `\d+\.\d*` | Trailing Zero Optional                 |
|      2 | `\.\d+`    | No Leading Zero                        |
|      3 | `\d+(?=e)` | Integer (Scientific Notation Required) |

#### Optional Scientific Notation: `(?:...)?`

| Exp Ind |   Sign  | Integer |
|--------:|:-------:|---------|
|     `e` | `[+-]?` | `\d+`   |

See also:
    *   `REAL_MAG_DGT_RXS`
    *   `REAL_SCINOT_EXP_RXS`
    *   `REAL_SCINOT_RXS`, `REAL_SCINOT_RGX`
    *   `REAL_SCINOT_OPT_RXS`
    
"""

REAL_SCINOT_OPT_DGT_RXS: Final[str] = rf"{SIGN_OPT_RXS}{REAL_MAG_SCINOT_OPT_DGT_RXS}"
r"""
### Signed Real Number Digits Regex String (Optional Scientific Notation)

*   Supports All Valid Signed Real Formats
*   Not Integer, Complex, or Fraction
*   Supports Scientific Notation
    *   Integer Significand only allowed with Scientific Notation
    *   Optional Exponent Sign (`+` or `-`)
*   Does not include special values (e.g. `inf`, `nan`)
*   e.g.: `0.0`, `+0.0`, `-0.0`, `1.0`, `+23.456`, `-7e+2`, `+1.0e-3`, etc.
*   Usage: `re.compile(REAL_SCINOT_OPT_RXS, flags=re.IGNORECASE)`

### Pattern: `[+-]?(?:\d+\.\d*|\.\d+|\d+(?=e))(?:e[+-]?\d+)?`

#### Signed Real Number Regex Structure:

|   Sign? | Significand Opts | Sci Not?   |
|--------:|-----------------:|:-----------|
| `[+-]?` |  `(?:...\|...)`  | `(?:...)?` |

#### Significand Non-Capturing Option Group: `(?:...|...)`

| Option |    Regex   | Description                            |
|-------:|------------|:---------------------------------------|
|      1 | `\d+\.\d*` | Trailing Zero Optional                 |
|      2 | `\.\d+`    | No Leading Zero                        |
|      3 | `\d+(?=e)` | Integer (Scientific Notation Required) |

#### Optional Scientific Notation: `(?:...)?`

| Exp Ind |   Sign  | Integer |
|--------:|:-------:|---------|
|     `e` | `[+-]?` | `\d+`   |

See also:
    *   `REAL_MAG_SCINOT_OPT_DGT_RXS`
    *   `REAL_SCINOT_RXS`, `REAL_SCINOT_RGX`
"""

REAL_RXS: Final[str] = rf"{SIGN_OPT_RXS}(?:{REAL_MAG_SCINOT_OPT_DGT_RXS}|{REAL_SPEC_RXS})"
r"""
### Signed Real Regex String

*   Supports All Valid Signed Real Formats
*   Not Integer, Complex, or Fraction
*   Regular Signed Real Numbers:
    *   e.g.: `0.0`, `+0.0`, `-0.0`, `1.0`, `+23.456`, `-7.`, `.89`, etc.
*   Supports Scientific Notation
    *   Integer Significand only allowed with Scientific Notation
    *   Optional Exponent Sign (`+` or `-`)
    *   e.g.: `0.0e0`, `-0.0e+0`, `+0.0e-0`, `1.0e+2`, `+3.456e-3`, `-7e8`, `9.e+10`, `.23e-4`, etc.
*   Supports Special Values:
    *   `inf`, `infinity`, `nan`
    *   e.g.: `inf`, `-inf`, `infinity`, `-infinity`, `nan`
*   Usage: `re.compile(REAL_RXS, flags=re.IGNORECASE)`

### Pattern: `[+-]?(?:(?:\d+\.\d*|\.\d+|\d+(?=e))(?:e[+-]?\d+)?|inf(?:inity)?|nan)`

#### Signed Real Regex Structure:

|   Sign? | Real Opts      |
|--------:|:---------------|
| `[+-]?` | `(?:...\|...)` |

#### Real Non-Capturing Option Group: `(?:...|...)`

| Option |       Regex        | Body    | NC Suffix? | Description  |
|-------:|--------------------|--------:|:-----------|:-------------|
|      1 | See Real Num Table | Options | Exponent   | Real Number  |
|      2 | `inf(?:inity)?`    |   `inf` | `inity`    | Infinity     |
|      3 | `nan`              |   `nan` |            | Not a Number |

#### Real Number Regex Structure:
| Significand Opts | Sci Not?   |
|-----------------:|:-----------|
|   `(?:...\|...)` | `(?:...)?` |

#### Significand Non-Capturing Option Group: `(?:...|...)`

| Option |    Regex   | Description                            |
|-------:|------------|:---------------------------------------|
|      1 | `\d+\.\d*` | Trailing Zero Optional                 |
|      2 | `\.\d+`    | No Leading Zero                        |
|      3 | `\d+(?=e)` | Integer (Scientific Notation Required) |

#### Optional Scientific Notation: `(?:...)?`

| Exp Ind |   Sign  | Integer |
|--------:|:-------:|---------|
|     `e` | `[+-]?` | `\d+`   |

See also:
    *   `REAL_MAG_SCINOT_OPT_DGT_RXS`
    *   `REAL_SPEC_RXS`
    *   `REAL_RGX`
"""

REAL_RGX: Final[Pattern] = compile(rf"^\s*{REAL_RXS}\s*$", flags=IGNORECASE)
r"""
### Signed Real Regex Pattern

*   Supports All Valid Signed Real Formats
*   Not Integer, Complex, or Fraction
*   Regular Signed Real Numbers:
    *   e.g.: `0.0`, `+0.0`, `-0.0`, `1.0`, `+23.456`, `-7.`, `.89`, etc.
*   Supports Scientific Notation
    *   Integer Significand only allowed with Scientific Notation
    *   Optional Exponent Sign (`+` or `-`)
    *   e.g.: `0.0e0`, `-0.0e+0`, `+0.0e-0`, `1.0e+2`, `+3.456e-3`, `-7e8`, `9.e+10`, `.23e-4`, etc.
*   Supports Special Values:
    *   `inf`, `infinity`, `nan`
    *   e.g.: `inf`, `-inf`, `infinity`, `-infinity`, `nan`
*   Usage: `REAL_RGX.match("1.0e-3")`

### Pattern: `^\s*[+-]?(?:(?:\d+\.\d*|\.\d+|\d+(?=e))(?:e[+-]?\d+)?|inf(?:inity)?|nan)\s*$`

#### Signed Real Regex Structure:

| Prefix? |  Sign?  |    Real Opts   | Suffix? |
|--------:|:-------:|:--------------:|:--------|
|  `^\s*` | `[+-]?` | `(?:...\|...)` | `\s*$`  |

#### Real Non-Capturing Option Group: `(?:...|...)`

| Option |       Regex        | Body    | NC Suffix? | Description  |
|-------:|--------------------|--------:|:-----------|:-------------|
|      1 | See Real Num Table | Options | Exponent   | Real Number  |
|      2 | `inf(?:inity)?`    |   `inf` | `inity`    | Infinity     |
|      3 | `nan`              |   `nan` |            | Not a Number |

#### Real Number Regex Structure:
| Significand Opts | Sci Not?   |
|-----------------:|:-----------|
|   `(?:...\|...)` | `(?:...)?` |

#### Significand Non-Capturing Option Group: `(?:...|...)`

| Option |    Regex   | Description                            |
|-------:|------------|:---------------------------------------|
|      1 | `\d+\.\d*` | Trailing Zero Optional                 |
|      2 | `\.\d+`    | No Leading Zero                        |
|      3 | `\d+(?=e)` | Integer (Scientific Notation Required) |

#### Optional Scientific Notation: `(?:...)?`

| Exp Ind |   Sign  | Integer |
|--------:|:-------:|---------|
|     `e` | `[+-]?` | `\d+`   |

See also:
    *   `REAL_RXS`
"""

### Booleans ###

BOOL_TRUE_RXS: Final[str] = r"t(?:true)?"
r"""
### True Boolean Value Regex String

*   e.g.: `t`, `T`, `true`, `True`, `TRUE`, etc.
*   Usage: `re.compile(BOOL_TRUE_RXS, flags=re.IGNORECASE)`

### Pattern: `t(?:rue)?`

#### True Boolean Regex Structure:
| Letter | Suffix? |
|-------:|:--------|
|    `t` | `rue`   |

See also:
    *   `BOOL_TRUE_RGX`
    *   `BOOL_TRUE_EXT_RXS`, `BOOL_TRUE_EXT_RGX`
    *   `BOOL_FALSE_RXS`, `BOOL_FALSE_RGX`
    *   `BOOL_FALSE_EXT_RXS`, `BOOL_FALSE_EXT_RGX`
    *   `BOOL_RXS`, `BOOL_RGX`
    *   `BOOL_EXT_RXS`, `BOOL_EXT_RGX`
"""

BOOL_TRUE_RGX: Final[Pattern] = compile(rf"^\s*({BOOL_TRUE_RXS})\s*$", flags=IGNORECASE)
r"""
### True Boolean Regex

*   e.g.: `t`, `T`, `true`, `True`, `TRUE`, etc.
*   Usage: `re.compile(BOOL_TRUE_RXS, flags=re.IGNORECASE)`

### Pattern: `^\s*t(?:rue)?\s*$`

#### True Boolean Regex Structure:

| Prefix? | Letter | Suffix? | Suffix? |
|--------:|:------:|:-------:|:--------|
|  `^\s*` |   `t`  |  `rue`  | `\s*$`  |

See also:
    *   `BOOL_TRUE_RXS`
    *   `BOOL_TRUE_EXT_RXS`, `BOOL_TRUE_EXT_RGX`
    *   `BOOL_FALSE_RXS`, `BOOL_FALSE_RGX`
    *   `BOOL_FALSE_EXT_RXS`, `BOOL_FALSE_EXT_RGX`
    *   `BOOL_RXS`, `BOOL_RGX`
    *   `BOOL_EXT_RXS`, `BOOL_EXT_RGX`
"""

BOOL_TRUE_EXT_RXS: Final[str] = rf"{BOOL_TRUE_RXS}|y(?:es)?|on?|e(?:nable)?"
r"""
### True Boolean Regex String

*   Words: `true`, `yes`, `on`, `enable`
*   Values:
    *   TRUE:   `t`, `T`, `true`, `True`, `TRUE`, etc.
    *   YES:    `y`, `Y`, `yes`, `Yes`, `YES`, etc.
    *   ON:     `o`, `O`, `on`, `On`, `ON`, etc.
    *   ENABLE: `e`, `E`, `enable`, `Enable`, `ENABLE`, etc.
*   Usage: `re.compile(BOOL_TRUE_EXT_RXS, flags=re.IGNORECASE)`

### Pattern: `t(?:rue)?|y(?:es)?|on?|e(?:nable)?`

#### True Boolean Regex Option Series: `...|...`
| Option |    Regex      | Letter | Suffix? | Description            |
|-------:|---------------|-------:|:--------|:-----------------------|
|      1 | `t(?:rue)?`   |    `t` | `rue`   | True                   |
|      2 | `y(?:es)?`    |    `y` | `es`    | Yes                    |
|      3 | `on?`         |    `o` | `n`     | On                     |
|      4 | `e(?:nable)?` |    `e` | `nable` | Enable                 |

See also:
    *   `BOOL_TRUE_RXS`, `BOOL_TRUE_RGX`
    *   `BOOL_TRUE_EXT_RGX`
    *   `BOOL_FALSE_RXS`, `BOOL_FALSE_RGX`
    *   `BOOL_FALSE_EXT_RXS`, `BOOL_FALSE_EXT_RGX`
    *   `BOOL_RXS`, `BOOL_RGX`
    *   `BOOL_EXT_RXS`, `BOOL_EXT_RGX`
"""

BOOL_TRUE_RGX: Final[Pattern] = compile(rf"^\s*({BOOL_TRUE_EXT_RXS})\s*$", flags=IGNORECASE)
r"""
### True Boolean Regex Pattern

*   Words: `true`, `yes`, `on`, `enable`
*   Values:
    *   TRUE:   `t`, `T`, `true`, `True`, `TRUE`, etc.
    *   YES:    `y`, `Y`, `yes`, `Yes`, `YES`, etc.
    *   ON:     `o`, `O`, `on`, `On`, `ON`, etc.
    *   ENABLE: `e`, `E`, `enable`, `Enable`, `ENABLE`, etc.
*   Usage: `re.compile(BOOL_TRUE_EXT_RGX, flags=re.IGNORECASE)`

### Pattern: `^\s*t(?:rue)?|y(?:es)?|on?|e(?:nable)?\s*$`

#### True Boolean Regex Structure:
| Prefix? |    True Opts   | Suffix? |
|--------:|:--------------:|:--------|
|  `^\s*` | `(?:...\|...)` | `\s*$`  |

#### True Boolean Regex Option Group: `(...|...)`

| Option |    Regex      | Letter | Suffix? | Description            |
|-------:|---------------|-------:|:--------|:-----------------------|
|      1 | `t(?:rue)?`   |    `t` | `rue`   | True                   |
|      2 | `y(?:es)?`    |    `y` | `es`    | Yes                    |
|      3 | `on?`         |    `o` | `n`     | On                     |
|      4 | `e(?:nable)?` |    `e` | `nable` | Enable                 |

See also:
    *   `BOOL_TRUE_RXS`, `BOOL_TRUE_RGX`
    *   `BOOL_TRUE_EXT_RGX`
    *   `BOOL_FALSE_RXS`, `BOOL_FALSE_RGX`
    *   `BOOL_FALSE_EXT_RXS`, `BOOL_FALSE_EXT_RGX`
    *   `BOOL_RXS`, `BOOL_RGX`
    *   `BOOL_EXT_RXS`, `BOOL_EXT_RGX`
"""

BOOL_FALSE_RXS: Final[str] = r"f(?:alse)?"
r"""
### False Boolean Value Regex String

*   e.g.: `f`, `F`, `false`, `False`, `FALSE`, etc.
*   Usage: `re.compile(BOOL_FALSE_RXS, flags=re.IGNORECASE)`

### Pattern: `f(?:alse)?`

#### False Boolean Regex Structure:
| Letter | Suffix? |
|-------:|:--------|
|    `f` | `alse`  |

See also:
    *   `BOOL_TRUE_RXS`, `BOOL_TRUE_RGX`
    *   `BOOL_TRUE_EXT_RXS`, `BOOL_TRUE_EXT_RGX`
    *   `BOOL_FALSE_RGX`
    *   `BOOL_FALSE_EXT_RXS`, `BOOL_FALSE_EXT_RGX`
    *   `BOOL_RXS`, `BOOL_RGX`
    *   `BOOL_EXT_RXS`, `BOOL_EXT_RGX`
"""

BOOL_FALSE_RGX: Final[Pattern] = compile(rf"^\s*({BOOL_FALSE_RXS})\s*$", flags=IGNORECASE)
r"""
### False Boolean Regex Pattern

*   e.g.: `f`, `F`, `false`, `False`, `FALSE`, etc.
*   Usage: `BOOL_FALSE_RGX.match("false")`

### Pattern: `^\s*f(?:alse)?\s*$`

#### False Boolean Regex Structure:

| Prefix? | Letter | Word Suffix? | Suffix? |
|--------:|:------:|:------------:|:--------|
|  `^\s*` |   `f`  |    `alse`    |  `\s*$` |

See also:
    *   `BOOL_TRUE_RXS`, `BOOL_TRUE_RGX`
    *   `BOOL_TRUE_EXT_RXS`, `BOOL_TRUE_EXT_RGX`
    *   `BOOL_FALSE_RXS`
    *   `BOOL_FALSE_EXT_RXS`, `BOOL_FALSE_EXT_RGX`
    *   `BOOL_RXS`, `BOOL_RGX`
    *   `BOOL_EXT_RXS`, `BOOL_EXT_RGX`
"""

"""
See also:
    *   `BOOL_TRUE_RXS`, `BOOL_TRUE_RGX`
    *   `BOOL_TRUE_EXT_RXS`, `BOOL_TRUE_EXT_RGX`
    *   `BOOL_FALSE_RXS`, `BOOL_FALSE_RGX`
    *   `BOOL_FALSE_EXT_RXS`, `BOOL_FALSE_EXT_RGX`
    *   `BOOL_RXS`, `BOOL_RGX`
    *   `BOOL_EXT_RXS`, `BOOL_EXT_RGX`
"""

BOOL_RXS: Final[str] = r"t(?:rue)?|f(?:alse)?"
r"""
### Boolean Regex String

*   Supports All Valid Boolean Formats
*   Notes:
    *   This does not support 1 or 0 because they would be ambiguous with integers
    *   Supported words: true, false
*   e.g.: `true`, `True`, `TRUE`, `false`, `False`, `FALSE`, etc.
*   Usage: `re.compile(BOOL_RXS, flags=re.IGNORECASE)`

### Pattern: `t(?:rue)?|f(?:alse)?`

#### Boolean Option Series: `...|...`

| Option |    Regex    | Letter | Suffix? | Description            |
|-------:|-------------|-------:|:--------|:-----------------------|
|      1 | `t(?:rue)?` |    `t` | `rue`   | True                   |
|      2 | `f(?:alse)?`|    `f` | `alse`  | False                  |
"""

BOOL_EXT_RXS: Final[str] = rf"{BOOL_RXS}|y(?:es)?|n(?:o)?|on?|o(ff)?|e(?:nable)?|d(?:isable)?"
r"""
### Boolean Regex String

*   Supports All Valid Boolean Formats
*   Notes:
    *   This does not support 1 or 0 because they would be ambiguous with integers
    *   Compile this regex string with the `IGNORECASE` flag
    *   Supported boolean pairs:
        *   True/False: `t`, `F`, `true`, `FALSE`, `True`, etc.
        *   Yes/No: `y`, `n`, `yes`, `no`, `YES`, `No`, etc.
        *   On/Off: `o`, `n`, `on`, `off`, `ON`, `Off`, etc.
        *   Enable/Disable: `e`, `d`, `enable`, `disable`, `ENABLE`, `DISABLE`, etc.
*   Pattern
    *   `...|...`           <br/>Option Series
        *   `t`             <br/>t for True
        *   `(?:...)`       <br/>Non-Capturing Option Group
            *   `rue`       <br/>True spelled out
        *   `f`             <br/>f for False
        *   `(?:...)`       <br/>Non-Capturing Option Group
            *   `alse`      <br/>False spelled out
        *   `y`             <br/>y for Yes
        *   `(?:...)`       <br/>Non-Capturing Option Group
            *   `es`        <br/>Yes spelled out
        *   `n`             <br/>n for No
        *   `(?:...)`       <br/>Non-Capturing Option Group
            *   `o`         <br/>No spelled out
        *   `e`             <br/>e for Enable
        *   `(?:...)`       <br/>Non-Capturing Option Group
            *   `nable`     <br/>Enable spelled out
        *   `d`             <br/>d for Disable
        *   `(?:...)`       <br/>Non-Capturing Option Group
            *   `isable`    <br/>Disable spelled out
"""

BOOL_RGX: Final[Pattern] = compile(rf"^\s*({BOOL_RXS})\s*$", flags=IGNORECASE)
r"""
### Boolean Regex

*   Supports All Valid Boolean Formats
*   Notes:
    *   This does not support 1 or 0 because they would be ambiguous with integers
    *   Compile this regex string with the `IGNORECASE` flag
    *   Supported words: true, false, yes, no, enable, disable
*   e.g.: `true`, `True`, `TRUE`, `false`, `False`, `FALSE`, etc.

### Pattern: `^\s*(t(?:rue)?|f(?:alse)?|y(?:es)?|n(?:o)?|e(?:nable)?|d(?:isable)?)\s*$`

    *   `^`                     <br/>Start
    *   `\s*`                   <br/>Optional Whitespace
    0.  `(...|...)`             <br/>Capture Option Group 0
            *   `t`             <br/>t for True
            *   `(?:...)`       <br/>Non-Capturing Option Group
                *   `rue`       <br/>True spelled out
            *   `f`             <br/>f for False
            *   `(?:...)`       <br/>Non-Capturing Option Group
                *   `alse`      <br/>False spelled out
            *   `y`             <br/>y for Yes
            *   `(?:...)`       <br/>Non-Capturing Option Group
                *   `es`        <br/>Yes spelled out
            *   `n`             <br/>n for No
            *   `(?:...)`       <br/>Non-Capturing Option Group
                *   `o`         <br/>No spelled out
            *   `e`             <br/>e for Enable
            *   `(?:...)`       <br/>Non-Capturing Option Group
                *   `nable`     <br/>Enable spelled out
            *   `d`             <br/>d for Disable
            *   `(?:...)`       <br/>Non-Capturing Option Group
                *   `isable`    <br/>Disable spelled out
    *   `\s*`                   <br/>Optional Whitespace
    *   `$`                     <br/>End
"""

### Complex Numbers ###

COMPLEX_RXS: Final[str] = rf"[+-]?(?:{__REAL_NON_SPEC_RXS})[+-]{__REAL_NON_SPEC_RXS}j"
r"""
### Complex Number Regex String

*   Supports All Valid Complex Formats
*   Complex Numbers Only
*   Leading Sign (optional `+` or `-`)
*   Real and Imaginary Parts
    *   e.g.: `1+2j`, `-3.5-4.5j`, `0.0+0.0j`, `1e-3+2e+3j`, etc.
*   Note: Compile this regex string with the `IGNORECASE` flag

### Pattern: `[+-]?(?:\d+\.\d*|\.\d+|\d+(?=e))(?:e[+-]?\d+)?[+-](?:\d+\.\d*|\.\d+|\d+(?=e))(?:e[+-]?\d+)?j`

    *   Real Part:
        *   `[+-]?`         <br/>Optional Sign
        *   `(?:...|...)`   <br/>Non-Capturing Option Group
            *   `\d+\.\d*`  <br/>Real (trailing zero optional)
            *   `\.\d+`     <br/>Real (no leading zero)
            *   `\d+(?=e)`  <br/>Integer (only with Scientific Notation)
        *   `(?:...)?`      <br/>Optional Non-Capturing Element
            *   `e`         <br/>Exponent Indicator
            *   `[+-]?`     <br/>Optional Sign
            *   `\d+`       <br/>Integer
    *   Imaginary Part:
        *   `[+-]`          <br/>Sign
        *   `(?:...|...)`   <br/>Non-Capturing Option Group
            *   `\d+\.\d*`  <br/>Real (trailing zero optional)
            *   `\.\d+`     <br/>Real (no leading zero)
            *   `\d+(?=e)`  <br/>Integer (only with Scientific Notation)
        *   `(?:...)?`      <br/>Optional Non-Capturing Element
            *   `e`         <br/>Exponent Indicator
            *   `[+-]?`     <br/>Optional Sign
            *   `\d+`       <br/>Integer
        *   `j`             <br/>Imaginary Unit
"""
COMPLEX_RGX: Final[Pattern] = compile(rf"^\s*({COMPLEX_RXS})\s*$", flags=IGNORECASE)
r"""
### Complex Number Regex

*   Supports All Valid Complex Formats
*   Complex Numbers Only
*   Leading Sign (optional `+` or `-`)
*   Real and Imaginary Parts
    *   e.g.: `1+2j`, `-3.5-4.5j`, `0.0+0.0j`, `1e-3+2e+3j`, etc.
*   Note: Compile this regex string with the `IGNORECASE` flag

### Pattern: `^\s*([+-]?(?:\d+\.\d*|\.\d+|\d+(?=e))(?:e[+-]?\d+)?[+-](?:\d+\.\d*|\.\d+|\d+(?=e))(?:e[+-]?\d+)?j)\s*$`

    *   `^`                     <br/>Start
    *   `\s*`                   <br/>Optional Whitespace
    0.  `(...)`                 <br/>Capture Group 0
        *   Real Part:
            *   `[+-]?`         <br/>Optional Sign
            *   `(?:...|...)`   <br/>Non-Capturing Option Group
                *   `\d+\.\d*`  <br/>Real (trailing zero optional)
                *   `\.\d+`     <br/>Real (no leading zero)
                *   `\d+(?=e)`  <br/>Integer (only with Scientific Notation)
            *   `(?:...)?`      <br/>Optional Non-Capturing Element
                *   `e`         <br/>Exponent Indicator
                *   `[+-]?`     <br/>Optional Sign
                *   `\d+`       <br/>Integer
        *   Imaginary Part:
            *   `[+-]`          <br/>Sign
            *   `(?:...|...)`   <br/>Non-Capturing Option Group
                *   `\d+\.\d*`  <br/>Real (trailing zero optional)
                *   `\.\d+`     <br/>Real (no leading zero)
                *   `\d+(?=e)`  <br/>Integer (only with Scientific Notation)
            *   `(?:...)?`      <br/>Optional Non-Capturing Element
                *   `e`         <br/>Exponent Indicator
                *   `[+-]?`     <br/>Optional Sign
                *   `\d+`       <br/>Integer
            *   `j`             <br/>Imaginary Unit
    *   `\s*`                   <br/>Optional Whitespace
    *   `$`                     <br/>End
"""

### Fractions ###
FRACTION_RXS: Final[str] = r"[+-]?{__BASE_REAL_NON_SPEC_RXS}/{__BASE_REAL_NON_SPEC_RXS}"



### Real Numbers ###

REAL_RXS= r"[+-]?(?:(?:\d+\.\d*|\.\d+|\d+(?=e))(?:e[+-]?\d+)?|inf(?:inity)?|nan)"
r"""
### Real Number Regex String

*   Supports All Valid Real Formats
*   Sign (optional `+` or `-`)
*   Any Valid Real (Not Integer)
*   Scientific Notation Supported
    *   Significand:    digit followed by optional decimal and digits
    *   Exponent:       `e` followed by optional sign (`+` or `-`) and required int digits
*   Special Cases:
    *   Infinity:       inf or infinity
    *   Not a Number:   nan
*   Note: Compile this regex string with the `IGNORECASE` flag
*   e.g.: `1.0`, `+0.2`, `-34.56`, `7.8e+0`, `-9.0E-1`, `2.3e4`, `56E67`, `inf`, `-Infinity`, `NaN`, etc.
*   Pattern
    *   `[+-]?`                 <br/>Optional Sign
    *   Valid Real (Not Integer)
    *   `(?:...|...)`           <br/>Non-Capturing Option Group
        *   If Has Digits:
            *   `(?:...|...)`   <br/>Non-Capturing Option Group
                *   `\d+\.\d*`  <br/>Real (trailing zero optional)
                *   `\.\d+`     <br/>Real (no leading zero)
                *   `\d+(?=e)`  <br/>Integer (only with Scientific Notation)
            *   `(?:...)?`      <br/>Optional Non-Capturing Element
                *   `e`         <br/>Exponent Indicator
                *   `[+-]?`     <br/>Optional Sign
                *   `\d+`       <br/>Integer
        *   Special Cases:
            *   Infinity:
                *   `inf`       <br/>Infinity
                *   `(?:...)?`  <br/>Optional Non-Capturing Element
                    *   `inity` <br/>Infinity Suffix
            *   Not a Number:
                *   `nan`       <br/>Not a Number
"""
REAL_RGX= compile(rf"^\s*({REAL_RXS})\s*$",flags=IGNORECASE)
r"""
### Real Number Regex

*   Supports All Valid Real Formats
*   Sign (optional `+` or `-`)
*   Any Valid Real (Not Integer)
*   Scientific Notation Supported
    *   Significand:    digit followed by optional decimal and digits
    *   Exponent:       `e` followed by optional sign (`+` or `-`) and required int digits
*   Special Cases:
    *   Infinity:       inf or infinity
    *   Not a Number:   nan
*   Note: Compile this regex string with the `IGNORECASE` flag
*   e.g.: `1.0`, `+0.2`, `-34.56`, `7.8e+0`, `-9.0E-1`, `2.3e4`, `56E67`, `inf`, `-Infinity`, `NaN`, etc.

### Pattern: `^\s*([+-]?(?:(?:\d+\.\d*|\.\d+|\d+(?=e))(?:e[+-]?\d+)?|inf(?:inity)?|nan))\s*$`

    *   `^`                         <br/>Start
    *   `\s*`                       <br/>Optional Whitespace
    0.  `(...)`                     <br/>Capture Group 0
        *   `[+-]?`                 <br/>Optional Sign
        *   Valid Real (Not Integer)
        *   `(?:...|...)`           <br/>Non-Capturing Option Group
            *   If Has Digits:
                *   `(?:...|...)`   <br/>Non-Capturing Option Group
                    *   `\d+\.\d*`  <br/>Real (trailing zero optional)
                    *   `\.\d+`     <br/>Real (no leading zero)
                    *   `\d+(?=e)`  <br/>Integer (only with Scientific Notation)
                *   `(?:...)?`      <br/>Optional Non-Capturing Element
                    *   `e`         <br/>Exponent Indicator
                    *   `[+-]?`     <br/>Optional Sign
                    *   `\d+`       <br/>Integer
            *   Special Cases:
                *   Infinity:
                    *   `inf`       <br/>Infinity
                    *   `(?:...)?`  <br/>Optional Non-Capturing Element
                        *   `inity` <br/>Infinity Suffix
                *   Not a Number:
                    *   `nan`       <br/>Not a Number
    *   `\s*`                       <br/>Optional Whitespace
    *   `$`                         <br/>End
"""

REAL_BSC_RXS= r"[+-]?(?:\d+\.\d*|\.\d+)"
r"""
### Basic Real Number Regex String

*   Sign (optional `+` or `-`)
*   Strict Complete Real Only
*   Scientific Notation Not Supported
*   e.g.: `0.0`, `+0.0`, `-0.0`, `1.0`, `+0.2`, `-34.56`, `00.07`, etc.
*   Pattern
    *   `[+-]?`         <br/>Optional Sign
    *   `(?:...|...)`   <br/>Non-Capturing Option Group
        *   `\d+\.\d*`  <br/>Real (trailing zero optional)
        *   `\.\d+`     <br/>Real (no leading zero)
"""
REAL_BSC_RGX= compile(rf"^\s*({REAL_BSC_RXS})\s*$")
r"""
### Basic Real Regex

*   Sign (optional `+` or `-`)
*   Strict Complete Real Only
*   Scientific Notation Not Supported
*   e.g.: `0.0`, `+0.0`, `-0.0`, `1.0`, `+0.2`, `-34.56`, `00.07`, etc.

### Pattern: `^\s*([+-]?(?:\d+\.\d*|\.\d+))\s*$`

    *   `^`             <br/>Start
    *   `\s*`           <br/>Optional Whitespace
    0.  `(...)`         <br/>Capture Group 0
    *   `[+-]?`         <br/>Optional Sign
    *   `(?:...|...)`   <br/>Non-Capturing Option Group
        *   `\d+\.\d*`  <br/>Real (trailing zero optional)
        *   `\.\d+`     <br/>Real (no leading zero)
    *   `\s*`           <br/>Optional Whitespace
    *   `$`             <br/>End
"""

REAL_SCI_RXS= r"[+-]?(?:\d+\.?\d*|\.\d+)e[+-]?\d+"
r"""
### Scientific Notation Only Regex String

*   Sign (optional `+` or `-`)
*   e.g.: `0.0e+1`, `1.0E-2`, `2.3e4`, `56E67`, etc.
*   Note: Compile this regex string with the `IGNORECASE` flag
*   Pattern
    *   `[+-]?`         <br/>Optional Sign
    *   Real or Integer
    *   `(?:...|...)`   <br/>Non-Capturing Option Group
        *   `\d+\.?\d*` <br/>Integer or Real (trailing zero optional)
        *   `\.\d+`     <br/>Real (no leading zero)
    *   `e[+-]?\d+`     <br/>Scientific Notation
"""
REAL_SCI_RGX= compile(rf"^\s*({REAL_SCI_RXS})\s*$",flags=IGNORECASE)
r"""
### Scientific Notation Only Regex

*   Sign (optional `+` or `-`)
*   e.g.: `0.0e+1`, `1.0E-2`, `2.3e4`, `56E67`, etc.

### Pattern: `^\s*([+-]?(?:\d+\.?\d*|\.\d+)e[+-]?\d+)\s*$`

    *   `^`                 <br/>Start
    *   `\s*`               <br/>Optional Whitespace
    0.  `(...)`             <br/>Capture Group 0
        *   `[+-]?`         <br/>Optional Sign
        *   Real or Integer
        *   `(?:...|...)`   <br/>Non-Capturing Option Group
            *   `\d+\.?\d*` <br/>Integer or Real (trailing zero optional)
            *   `\.\d+`     <br/>Real (no leading zero)
        *   `e[+-]?\d+`     <br/>Scientific Notation
    *   `\s*`               <br/>Optional Whitespace
    *   `$`                 <br/>End
"""


### Real Numbers ###

REAL_RXS= r"[+-]?(?:(?:\d+\.\d*|\.\d+|\d+(?=e))(?:e[+-]?\d+)?|inf(?:inity)?|nan)"
r"""
### Real Number Regex String

*   Supports All Valid Real Formats
*   Sign (optional `+` or `-`)
*   Any Valid Real (Not Integer)
*   Scientific Notation Supported
    *   Significand:    digit followed by optional decimal and digits
    *   Exponent:       `e` followed by optional sign (`+` or `-`) and required int digits
*   Special Cases:
    *   Infinity:       inf or infinity
    *   Not a Number:   nan
*   Note: Compile this regex string with the `IGNORECASE` flag
*   e.g.: `1.0`, `+0.2`, `-34.56`, `7.8e+0`, `-9.0E-1`, `2.3e4`, `56E67`, `inf`, `-Infinity`, `NaN`, etc.
*   Pattern
    *   `[+-]?`                 <br/>Optional Sign
    *   Valid Real (Not Integer)
    *   `(?:...|...)`           <br/>Non-Capturing Option Group
        *   If Has Digits:
            *   `(?:...|...)`   <br/>Non-Capturing Option Group
                *   `\d+\.\d*`  <br/>Real (trailing zero optional)
                *   `\.\d+`     <br/>Real (no leading zero)
                *   `\d+(?=e)`  <br/>Integer (only with Scientific Notation)
            *   `(?:...)?`      <br/>Optional Non-Capturing Element
                *   `e`         <br/>Exponent Indicator
                *   `[+-]?`     <br/>Optional Sign
                *   `\d+`       <br/>Integer
        *   Special Cases:
            *   Infinity:
                *   `inf`       <br/>Infinity
                *   `(?:...)?`  <br/>Optional Non-Capturing Element
                    *   `inity` <br/>Infinity Suffix
            *   Not a Number:
                *   `nan`       <br/>Not a Number
"""
REAL_RGX= compile(rf"^\s*({REAL_RXS})\s*$",flags=IGNORECASE)
r"""
### Real Number Regex

*   Supports All Valid Real Formats
*   Sign (optional `+` or `-`)
*   Any Valid Real (Not Integer)
*   Scientific Notation Supported
    *   Significand:    digit followed by optional decimal and digits
    *   Exponent:       `e` followed by optional sign (`+` or `-`) and required int digits
*   Special Cases:
    *   Infinity:       inf or infinity
    *   Not a Number:   nan
*   Note: Compile this regex string with the `IGNORECASE` flag
*   e.g.: `1.0`, `+0.2`, `-34.56`, `7.8e+0`, `-9.0E-1`, `2.3e4`, `56E67`, `inf`, `-Infinity`, `NaN`, etc.

### Pattern: `^\s*([+-]?(?:(?:\d+\.\d*|\.\d+|\d+(?=e))(?:e[+-]?\d+)?|inf(?:inity)?|nan))\s*$`

    *   `^`                         <br/>Start
    *   `\s*`                       <br/>Optional Whitespace
    0.  `(...)`                     <br/>Capture Group 0
        *   `[+-]?`                 <br/>Optional Sign
        *   Valid Real (Not Integer)
        *   `(?:...|...)`           <br/>Non-Capturing Option Group
            *   If Has Digits:
                *   `(?:...|...)`   <br/>Non-Capturing Option Group
                    *   `\d+\.\d*`  <br/>Real (trailing zero optional)
                    *   `\.\d+`     <br/>Real (no leading zero)
                    *   `\d+(?=e)`  <br/>Integer (only with Scientific Notation)
                *   `(?:...)?`      <br/>Optional Non-Capturing Element
                    *   `e`         <br/>Exponent Indicator
                    *   `[+-]?`     <br/>Optional Sign
                    *   `\d+`       <br/>Integer
            *   Special Cases:
                *   Infinity:
                    *   `inf`       <br/>Infinity
                    *   `(?:...)?`  <br/>Optional Non-Capturing Element
                        *   `inity` <br/>Infinity Suffix
                *   Not a Number:
                    *   `nan`       <br/>Not a Number
    *   `\s*`                       <br/>Optional Whitespace
    *   `$`                         <br/>End
"""

REAL_BSC_RXS= r"[+-]?(?:\d+\.\d*|\.\d+)"
r"""
### Basic Real Number Regex String

*   Sign (optional `+` or `-`)
*   Strict Complete Real Only
*   Scientific Notation Not Supported
*   e.g.: `0.0`, `+0.0`, `-0.0`, `1.0`, `+0.2`, `-34.56`, `00.07`, etc.
*   Pattern
    *   `[+-]?`         <br/>Optional Sign
    *   `(?:...|...)`   <br/>Non-Capturing Option Group
        *   `\d+\.\d*`  <br/>Real (trailing zero optional)
        *   `\.\d+`     <br/>Real (no leading zero)
"""
REAL_BSC_RGX= compile(rf"^\s*({FLT_BSC_RXS})\s*$")
r"""
### Basic Real Regex

*   Sign (optional `+` or `-`)
*   Strict Complete Real Only
*   Scientific Notation Not Supported
*   e.g.: `0.0`, `+0.0`, `-0.0`, `1.0`, `+0.2`, `-34.56`, `00.07`, etc.

### Pattern: `^\s*([+-]?(?:\d+\.\d*|\.\d+))\s*$`

    *   `^`             <br/>Start
    *   `\s*`           <br/>Optional Whitespace
    0.  `(...)`         <br/>Capture Group 0
    *   `[+-]?`         <br/>Optional Sign
    *   `(?:...|...)`   <br/>Non-Capturing Option Group
        *   `\d+\.\d*`  <br/>Real (trailing zero optional)
        *   `\.\d+`     <br/>Real (no leading zero)
    *   `\s*`           <br/>Optional Whitespace
    *   `$`             <br/>End
"""

REAL_SCI_RXS= r"[+-]?(?:\d+\.?\d*|\.\d+)e[+-]?\d+"
r"""
### Scientific Notation Only Regex String

*   Sign (optional `+` or `-`)
*   e.g.: `0.0e+1`, `1.0E-2`, `2.3e4`, `56E67`, etc.
*   Note: Compile this regex string with the `IGNORECASE` flag
*   Pattern
    *   `[+-]?`         <br/>Optional Sign
    *   Real or Integer
    *   `(?:...|...)`   <br/>Non-Capturing Option Group
        *   `\d+\.?\d*` <br/>Integer or Real (trailing zero optional)
        *   `\.\d+`     <br/>Real (no leading zero)
    *   `e[+-]?\d+`     <br/>Scientific Notation
"""
REAL_SCI_RGX= compile(rf"^\s*({REAL_SCI_RXS})\s*$",flags=IGNORECASE)
r"""
### Scientific Notation Only Regex

*   Sign (optional `+` or `-`)
*   e.g.: `0.0e+1`, `1.0E-2`, `2.3e4`, `56E67`, etc.

### Pattern: `^\s*([+-]?(?:\d+\.?\d*|\.\d+)e[+-]?\d+)\s*$`

    *   `^`                 <br/>Start
    *   `\s*`               <br/>Optional Whitespace
    0.  `(...)`             <br/>Capture Group 0
        *   `[+-]?`         <br/>Optional Sign
        *   Real or Integer
        *   `(?:...|...)`   <br/>Non-Capturing Option Group
            *   `\d+\.?\d*` <br/>Integer or Real (trailing zero optional)
            *   `\.\d+`     <br/>Real (no leading zero)
        *   `e[+-]?\d+`     <br/>Scientific Notation
    *   `\s*`               <br/>Optional Whitespace
    *   `$`                 <br/>End
"""

### Generic Numbers ###

NUM_RXS: Final[str] = r"[+-]?(?:(?:\d+\.?\d*|\.\d+)(?:e[+-]?\d+)?|0(?:x[\da-f]+|b[01]+|o[0-7]+)|inf(?:inity)?|nan)"
r"""
### Number Regex String

*   Sign (optional `+` or `-`)
*   Basic Floats or Integer
    *   e.g.: `1`, `+2`, `-3`, `0`, `+0`, `-0`, `45`, `6.0`, `+7.8`, `-9.0`, `0.0`, `0.1`, `23.`, `.45`, etc.
*   Scientific Notation Supported
    *   e.g.: `0.0e+1`, `1.0E-2`, `2.3e4`, `56E67`, etc.
*   Non-Decimal Bases Supported:
    *   Hexadecimal:    `0x` followed by hex digits (`0-9`, `a-f`)
        *   e.g.: `0x1a`, `0X2F`, `0x3b`, etc.
    *   Binary:         `0b` followed by binary digits (`0-1`)
        *   e.g.: `0dec10`, `0B1101`, `0b1110`, etc.
    *   Octal:          `0o` followed by octal digits (`0-7`)
        *   e.g.: `0o12`, `0O34`, `0o56`, etc.
*   Special Cases:
    *   Infinity:       inf or infinity
    *   Not a Number:   nan
*   Note: Compile this regex string with the `IGNORECASE` flag
*   Pattern
    *   `[+-]?`                     <br/>Optional Sign
    *   Real or Integer
    *   `(?:...|...)`               <br/>Non-Capturing Option Group
        *   If Real or Base-10 Integer:
            *   `(?:...|...)`       <br/>Non-Capturing Option Group
                *   `\d+\.?\d*`     <br/>Integer or Real (trailing zero optional)
                *   `\.\d+`         <br/>Real (no leading zero)
                *   `(?:...)?`      <br/>Optional Non-Capturing Element
                    *   `e[+-]?\d+` <br/>Scientific Notation
        *   If Non-Decimal Bases:
            *   `0`                 <br/>Leading Zero
            *   `(?:...|...)`       <br/>Non-Capturing Option Group
                *   `x[\da-f]+`     <br/>Hexadecimal
                *   `b[01]+`        <br/>Binary
                *   `o[0-7]+`       <br/>Octal
        *   Special Cases:
            *   Infinity:           <br/>`inf` or `infinity`
            *   Not a Number:       <br/>`nan`
"""
NUM_RGX: Final[Pattern] = compile(rf"^\s*({NUM_RXS})\s*$", flags=IGNORECASE)
r"""
### Number Regex

*   Sign (optional `+` or `-`)
*   Basic Floats or Integer
    *   e.g.: `1`, `+2`, `-3`, `0`, `+0`, `-0`, `45`, `6.0`, `+7.8`, `-9.0`, `0.0`, `0.1`, `23.`, `.45`, etc.
*   Scientific Notation Supported
    *   e.g.: `0.0e+1`, `1.0E-2`, `2.3e4`, `56E67`, etc.
*   Non-Decimal Bases Supported:
    *   Hexadecimal:    `0x` followed by hex digits (`0-9`, `a-f`)
        *   e.g.: `0x1a`, `0X2F`, `0x3b`, etc.
    *   Binary:         `0b` followed by binary digits (`0-1`)
        *   e.g.: `0dec10`, `0B1101`, `0b1110`, etc.
    *   Octal:          `0o` followed by octal digits (`0-7`)
        *   e.g.: `0o12`, `0O34`, `0o56`, etc.
*   Special Cases:
    *   Infinity:       inf or infinity
    *   Not a Number:   nan

### Pattern: `^\s*([+-]?(?:(?:\d+\.?\d*|\.\d+)(?:e[+-]?\d+)?|0(?:x[\da-f]+|b[01]+|o[0-7]+)|inf(?:inity)?|nan))\s*$`

    *   `^`                             <br/>Start
    *   `\s*`                           <br/>Optional Whitespace
    0.  `(...)`                         <br/>Capture Group 0
        *   `[+-]?`                     <br/>Optional Sign
        *   Real or Integer
        *   `(?:...|...)`               <br/>Non-Capturing Option Group
            *   If Real or Base-10 Integer:
                *   `(?:...|...)`       <br/>Non-Capturing Option Group
                    *   `\d+\.?\d*`     <br/>Integer or Real (trailing zero optional)
                    *   `\.\d+`         <br/>Real (no leading zero)
                    *   `(?:...)?`      <br/>Optional Non-Capturing Element
                        *   `e[+-]?\d+` <br/>Scientific Notation
            *   If Non-Decimal Bases:
                *   `0`                 <br/>Leading Zero
                *   `(?:...|...)`       <br/>Non-Capturing Option Group
                    *   `x[\da-f]+`     <br/>Hexadecimal
                    *   `b[01]+`        <br/>Binary
                    *   `o[0-7]+`       <br/>Octal
            *   Special Cases:
                *   Infinity:           <br/>`inf` or `infinity`
                *   Not a Number:       <br/>`nan`
    *   `\s*`                           <br/>Optional Whitespace
    *   `$`                             <br/>End
"""

########## Functions ##########

def to_real_str(num: Union[Number, str]) -> str:
    """
    Format as a floating point string with appropriate precision.
    e.g. `1.0`, `-0.2`, `34.56`, `7.8e-5`, `-9.0E+16`, `123E+456`, `inf`, `-inf`, `nan`, etc.
    Uses as many significant digits as necessary to represent the number accurately.
    Scientific Notation is used for values with magnitudes:
    *   less than or equal to 1e-5
    *   greater than or equal to 1e16
    
    Args:
        num (Union[Number, str]): The float to format.
        
    Returns:
        str: The toted_str float.
    """
    return str(float(num))

def to_int_str(num: Union[Number, str]) -> str:
    """
    Format as an integer string.
    e.g. `0`, `-0`, `1`, `-2`, `34567`, etc.
    
    Args:
        num (Union[Number, str]): The integer to format.
        
    Returns:
        str: The toted_str integer.
    """
    return str(int(num))

def to_number_str(num: Union[Number, str]) -> str:
    """
    Format a number as a string with appropriate precision.
    
    Args:
        num (Union[Number, str]): The number to format.
    
    Returns:
        str: The toted_str number.
    """
    if is_real(num):
        return to_real_str(num)
    elif is_int(num):
        return to_int_str(num)
    else:
        raise ValueError(f"Invalid number: {num}")

def is_real(num: Union[Number, str]) -> bool:
    """
    Determine if the passed value represents a float number.
    
    Args:
        num (Union[Number, str]): The value to evaluate.
        
    Returns:
        bool: True if the value represents a float number, False otherwise.
    """
    return isinstance(num, float) or is_real_str(num)

def is_real_str(num: str) -> bool:
    """
    Determine if the string represents a float number.
    
    Args:
        num (str): The string to evaluate.
        
    Returns:
        bool: True if the string represents a float number, False otherwise.
    """
    return isinstance(num, str) and REAL_RGX.match(num)is not None

def is_real_basic(num: str) -> bool:
    """
    Determine if a string represents a basic float number. (i.e. no scientific notation)
    
    Args:
        num (str): The string to check.
        
    Returns:
        bool: True if the string represents a basic float number, False otherwise.
    """
    return REAL_BSC_RGX.match(num)is not None

def is_real_scinot(num: str) -> bool:
    """
    Determine if a string represents a scientific notation number.
    
    Args:
        num (str): The string to check.
        
    Returns:
        bool: True if the string represents a scientific notation number, False otherwise.
    """
    return REAL_SCI_RGX.match(num)is not None

def is_real_in_to_scinot_range_str(num: Union[Number, str]) -> bool:
    """
    Determine if the passed value is a floating point number in the range that format will display
    in scientific notation.
    * Less than or equal to 1e-5
    * Greater than or equal to 1e16
    
    Args:
        num (Union[Number, str]): The value to evaluate.
        
    Returns:
        bool: True if the value is in the scientific notation range, False otherwise.
    """
    if not is_real(num):
        return False
    
    num = float(num)
    return num <= 1e-5 or num >= 1e16

def is_int(num: Union[Number, str]) -> bool:
    """
    Determine if the passed value represents an integer number.
    
    Args:
        num (Union[Number, str]): The value to evaluate.
        
    Returns:
        bool: True if the value represents an integer number, False otherwise.
    """
    return type(num) == int or is_int_str(num)

def is_int_str(num: str) -> bool:
    """
    Determine if a string represents an integer number.
    
    Args:
        num (str): The string to check.
        
    Returns:
        bool: True if the string represents an integer number, False otherwise.
    """
    return INT_RGX.match(num) is not None

def is_int_dec(num: str) -> bool:
    """
    Determine if the passed string represents a decimal (base-10) integer.
    
    Args:
        num (str): The string to evaluate.
        
    Returns:
        bool: True if the string represents a decimal integer number, False otherwise.
    """
    return INT_DEC_RGX.match(num) is not None

def is_int_bin(num: str) -> bool:
    """
    Determine if the passed string represents a binary integer.
    
    Args:
        num (str): The string to evaluate.
        
    Returns:
        bool: True if the string represents a binary integer number, False otherwise.
    """
    return INT_BIN_RGX.match(num) is not None

def is_int_hex(num: str) -> bool:
    """
    Determine if the passed string represents a hexadecimal integer.
    
    Args:
        num (str): The string to evaluate.
        
    Returns:
        bool: True if the string represents a hexadecimal integer number, False otherwise.
    """
    return INT_HEX_RGX.match(num) is not None

def is_int_oct(num: str) -> bool:
    """
    Determine if the passed string represents an octal integer.
    
    Args:
        num (str): The string to evaluate.
        
    Returns:
        bool: True if the string represents an octal integer number, False otherwise.
    """
    return INT_OCT_RGX.match(num) is not None

def is_number(num: str) -> bool:
    """
    Determine if a string represents a number (either int or float).
    
    Args:
        num (str): The string to check.
        
    Returns:
        bool: True if the string represents a number, False otherwise.
    """
    return NUM_RGX.match(num) is not None

def to_float(num: Union[str, Number]) -> float:
    """
    Convert the passed value to a float.
    
    Args:
        num (Union[str, Number]): The value to convert.
        
    Returns:
        float: The converted float.
    """
    return float(num)


def to_number(num: Union[str, Number]) -> Number:
    """
    Convert a string to a number of the appropriate type (int or float) based on its format.
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
