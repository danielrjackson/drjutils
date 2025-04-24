"""
Number Utilities[+-]?

This module provides utilities for working with numbers (and strings that represent numbers).

Copyright 2025 Daniel Robert Jackson
"""

"""
Standard Libraries
"""
from numbers import Number
from re import compile, IGNORECASE
from typing import Union

__all__ = [
    "flt_bsc_rgx_str",
    "flt_bsc_rgx",
    "flt_rgx_str",
    "flt_rgx",
    "format_number",
    "int_bas_rgx_str",
    "int_bas_rgx",
    "int_bsc_rgx_str",
    "int_bsc_rgx",
    "int_rgx_str",
    "int_rgx",
    "is_basic_float",
    "is_basic_int",
    "is_float",
    "is_int",
    "is_non_decimal",
    "is_number",
    "is_scinot",
    "num_opl_rgx_str",
    "num_opl_rgx",
    "num_opt_rgx_str",
    "num_opt_rgx",
    "num_rgx_str",
    "num_rgx",
    "sci_rgx_str",
    "sci_rgx",
    "to_number"
]

### Floating point numbers ###

flt_bsc_rgx_str = r"[+-]?(?:\d+\.\d*|\.\d+)"
"""
### Basic Float
*   Sign (optional + or -)
*   Strict Complete Float Only
*   Scientific Notation Not Supported
*   e.g.: 0.0, +0.0, -0.0, 1.0, +0.2, -34.56, 00.07, etc.
*   Pattern
    *   `[+-]?`         <br/>Sign
    *   `(?:...|...)`   <br/>Non-Capturing Option Group
        *   `\d+\.\d*`  <br/>Float (trailing zero optional)
        *   `\.\d+`     <br/>Float (no leading zero)
"""
flt_bsc_rgx = compile(f"^\s*({flt_bsc_rgx_str})\s*$")
r"""
### Basic Float
*   Sign (optional + or -)
*   Strict Complete Float Only
*   Scientific Notation Not Supported
*   e.g.: 0.0, +0.0, -0.0, 1.0, +0.2, -34.56, 00.07, etc.
*   Pattern: `^\s*([+-]?(?:\d+\.\d*|\.\d+))\s*$`
    *   `^`             <br/>Start
    *   `\s*`           <br/>Optional Whitespace
    0.  `(...)`         <br/>Capture Group 0
    *   `[+-]?`         <br/>Sign
    *   `(?:...|...)`   <br/>Non-Capturing Option Group
        *   `\d+\.\d*`  <br/>Float (trailing zero optional)
        *   `\.\d+`     <br/>Float (no leading zero)
    *   `\s*`           <br/>Optional Whitespace
    *   `$`             <br/>End
"""

flt_rgx_str = r"[+-]?(?:(?:\d+\.\d*|\.\d+|\d+(?=e))(?:e[+-]?\d+)?|inf(?:inity)?|nan)"
"""
### Float Number
*   Supports All Valid Float Formats
*   Sign (optional + or -)
*   Any Valid Float (Not Integer)
*   Scientific Notation Supported
    *   Significand:    digit followed by optional decimal and digits
    *   Exponent:       e followed by optional sign (+ or -) and required int digits
*   Special Cases:
    *   Infinity:       inf or infinity
    *   Not a Number:   nan
*   Be sure to use the `IGNORECASE` flag when compiling this regex
*   e.g.: 1.0, +0.2, -34.56, 7.8e+0, -9.0E-1, 2.3e4, 56E67, inf, -Infinity, NaN, etc.
*   Pattern
    *   `[+-]?`                 <br/>Sign
    *   Valid Float (Not Integer)
    *   `(?:...|...)`           <br/>Non-Capturing Option Group
        *   If Has Digits:
            *   `(?:...|...)`   <br/>Non-Capturing Option Group
                *   `\d+\.\d*`  <br/>Float (trailing zero optional)
                *   `\.\d+`     <br/>Float (no leading zero)
                *   `\d+(?=e)`  <br/>Integer (only with Scientific Notation)
            *   `(?:...)?`      <br/>Optional Non-Capturing Group
                *   `e`         <br/>Exponent Indicator
                *   `[+-]?`     <br/>Sign
                *   `\d+`       <br/>Integer
        *   Special Cases:
            *   Infinity:
                *   `inf`       <br/>Infinity
                *   `(?:...)?`  <br/>Optional Non-Capturing Group
                    *   `inity` <br/>Infinity Suffix
            *   Not a Number:
                *   `nan`       <br/>Not a Number
"""
flt_rgx = compile(f"^\s*({flt_rgx_str})\s*$", flags=IGNORECASE)
r"""
### Float Number
*   Supports All Valid Float Formats
*   Sign (optional + or -)
*   Any Valid Float (Not Integer)
*   Scientific Notation Supported
    *   Significand:    digit followed by optional decimal and digits
    *   Exponent:       e followed by optional sign (+ or -) and required int digits
*   Special Cases:
    *   Infinity:       inf or infinity
    *   Not a Number:   nan
*   Be sure to use the `IGNORECASE` flag when compiling this regex
*   e.g.: 1.0, +0.2, -34.56, 7.8e+0, -9.0E-1, 2.3e4, 56E67, inf, -Infinity, NaN, etc.
*   Pattern: `^\s*([+-]?(?:(?:\d+\.\d*|\.\d+|\d+(?=e))(?:e[+-]?\d+)?|inf(?:inity)?|nan))\s*$`
    *   `^`                         <br/>Start
    *   `\s*`                       <br/>Optional Whitespace
    0.  `(...)`                     <br/>Capture Group 0
        *   `[+-]?`                 <br/>Sign
        *   Valid Float (Not Integer)
        *   `(?:...|...)`           <br/>Non-Capturing Option Group
            *   If Has Digits:
                *   `(?:...|...)`   <br/>Non-Capturing Option Group
                    *   `\d+\.\d*`  <br/>Float (trailing zero optional)
                    *   `\.\d+`     <br/>Float (no leading zero)
                    *   `\d+(?=e)`  <br/>Integer (only with Scientific Notation)
                *   `(?:...)?`      <br/>Optional Non-Capturing Group
                    *   `e`         <br/>Exponent Indicator
                    *   `[+-]?`     <br/>Sign
                    *   `\d+`       <br/>Integer
            *   Special Cases:
                *   Infinity:
                    *   `inf`       <br/>Infinity
                    *   `(?:...)?`  <br/>Optional Non-Capturing Group
                        *   `inity` <br/>Infinity Suffix
                *   Not a Number:
                    *   `nan`       <br/>Not a Number
    *   `\s*`                       <br/>Optional Whitespace
    *   `$`                         <br/>End
"""

### Integers ###

int_bas_rgx_str = r"[+-]?0(?:x[\da-f]+|b[01]+|o[0-7]+)"
"""
### Integer Number (Non-Decimal Bases Only)
*   Sign (optional + or -)
*   Non-Decimal Bases:
    *   Hexadecimal:    0x followed by hex digits (0-9, a-f)
        *   e.g.: 0x1a, 0X2F, 0x3b, etc.
    *   Binary:         0b followed by binary digits (0-1)
        *   e.g.: 0b1010, 0B1101, 0b1110, etc.
    *   Octal:          0o followed by octal digits (0-7)
        *   e.g.: 0o12, 0O34, 0o56, etc.
*   Be sure to use the `IGNORECASE` flag when compiling this regex
*   Pattern
    *   `[+-]?`         <br/>Sign
    *   `0`             <br/>Leading Zero
    *   `(?:...|...)`   <br/>Non-Capturing Option Group
        *   `x[\da-f]+` <br/>Hexadecimal
        *   `b[01]+`    <br/>Binary
        *   `o[0-7]+`   <br/>Octal
"""
int_bas_rgx = compile(f"^\s*({int_bas_rgx_str})\s*$", flags=IGNORECASE)
r"""
### Integer Number (Non-Decimal Bases Only)
*   Sign (optional + or -)
*   Non-Decimal Bases:
    *   Hexadecimal:    0x followed by hex digits (0-9, a-f)
        *   e.g.: 0x1a, 0X2F, 0x3b, etc.
    *   Binary:         0b followed by binary digits (0-1)
        *   e.g.: 0b1010, 0B1101, 0b1110, etc.
    *   Octal:          0o followed by octal digits (0-7)
        *   e.g.: 0o12, 0O34, 0o56, etc.
*   Pattern: `^\s*([+-]?0(?:x[\da-f]+|b[01]+|o[0-7]+))\s*$`
    *   `^`                 <br/>Start
    *   `\s*`               <br/>Optional Whitespace
    0.  `(...)`             <br/>Capture Group 0
        *   `[+-]?`         <br/>Sign
        *   `0`             <br/>Leading Zero
        *   `(?:...|...)`   <br/>Non-Capturing Option Group
            *   `x[\da-f]+` <br/>Hexadecimal
            *   `b[01]+`    <br/>Binary
            *   `o[0-7]+`   <br/>Octal
    *   `\s*`               <br/>Optional Whitespace
    *   `$`                 <br/>End
"""

int_bsc_rgx_str = r"[+-]?\d+"
"""
### Integer Number (Basic)
*   Sign (optional + or -)
*   Integer Only
*   e.g.: 1, +2, -3, +0, -0, 42, 0012, etc.
*   Pattern
    *   `[+-]?` <br/>Sign
    *   `\d+`   <br/>Integer
"""
int_bsc_rgx = compile(f"^\s*({int_bsc_rgx_str})\s*$")
r"""
### Integer Number (Basic)
*   Sign (optional + or -)
*   Integer Only
*   e.g.: 1, +2, -3, +0, -0, 42, 0012, etc.
*   Pattern: `^\s*([+-]?\d+)\s*$`
    *   `^`         <br/>Start
    *   `\s*`       <br/>Optional Whitespace
    0.  `(...)`     <br/>Capture Group 0
        *   `[+-]?` <br/>Sign
        *   `\d+`   <br/>Integer
    *   `\s*`       <br/>Optional Whitespace
    *   `$`         <br/>End
"""

int_rgx_str = r"[+-]?(?:\d+|0(?:x[\da-f]+|b[01]+|o[0-7]+))"
"""
### Integer Number
*   Supports All Valid Integer Formats
*   Sign (optional + or -)
*   Integers Only
    *   e.g.: 1, +2, -3, +0, -0, 42, 0012, etc.
*   Supports Non-Decimal Bases:
    *   Hexadecimal:    0x followed by hex digits (0-9, a-f)
        *   e.g.: 0x1a, 0X2F, 0x3b, etc.
    *   Binary:         0b followed by binary digits (0-1)
        *   e.g.: 0b1010, 0B1101, 0b1110, etc.
    *   Octal:          0o followed by octal digits (0-7)
        *   e.g.: 0o12, 0O34, 0o56, etc.
*   Be sure to use the `IGNORECASE` flag when compiling this regex
*   Pattern
    *   `[+-]?`                 <br/>Sign
    *   `(?:...|...)`           <br/>Non-Capturing Option Group
        *   `\d+`               <br/>Integer
        *   Non-Decimal Bases:
            *   `0`             <br/>Leading Zero
            *   `(?:...|...)`   <br/>Non-Capturing Option Group
                *   `x[\da-f]+` <br/>Hexadecimal
                *   `b[01]+`    <br/>Binary
                *   `o[0-7]+`   <br/>Octal
"""
int_rgx = compile(f"^\s*({int_rgx_str})\s*$", flags=IGNORECASE)
r"""
### Integer Number
*   Supports All Valid Integer Formats
*   Sign (optional + or -)
*   Integers Only
    *   e.g.: 1, +2, -3, +0, -0, 42, 0012, etc.
*   Supports Non-Decimal Bases:
    *   Hexadecimal:    0x followed by hex digits (0-9, a-f)
        *   e.g.: 0x1a, 0X2F, 0x3b, etc.
    *   Binary:         0b followed by binary digits (0-1)
        *   e.g.: 0b1010, 0B1101, 0b1110, etc.
    *   Octal:          0o followed by octal digits (0-7)
        *   e.g.: 0o12, 0O34, 0o56, etc.
*   Pattern: `^\s*([+-]?(?:\d+|0(?:x[\da-f]+|b[01]+|o[0-7]+)))\s*$`
    *   `^`                         <br/>Start
    *   `\s*`                       <br/>Optional Whitespace
    0.  `(...)`                     <br/>Capture Group 0
        *   `[+-]?`                 <br/>Sign
        *   `(?:...|...)`           <br/>Non-Capturing Option Group
            *   `\d+`               <br/>Integer
            *   Non-Decimal Bases:
                *   `0`             <br/>Leading Zero
                *   `(?:...|...)`   <br/>Non-Capturing Option Group
                    *   `x[\da-f]+` <br/>Hexadecimal
                    *   `b[01]+`    <br/>Binary
                    *   `o[0-7]+`   <br/>Octal
    *   `\s*`                       <br/>Optional Whitespace
    *   `$`                         <br/>End
"""

### Generic Numbers (Floats or Ints) ###

num_rgx_str = r"[+-]?(?:(?:\d+\.?\d*|\.\d+)(?:e[+-]?\d+)?|0(?:x[\da-f]+|b[01]+|o[0-7]+)|inf(?:inity)?|nan)"
"""
### Number
*   Sign (optional + or -)
*   Basic Floats or Integer
    *   e.g.: 1, +2, -3, 0, +0, -0, 45, 6.0, +7.8, -9.0, 0.0, 0.1, 23., .45, etc.
*   Scientific Notation Supported
    *   e.g.: 0.0e+1, 1.0E-2, 2.3e4, 56E67, etc.
*   Non-Decimal Bases Supported:
    *   Hexadecimal:    0x followed by hex digits (0-9, a-f)
        *   e.g.: 0x1a, 0X2F, 0x3b, etc.
    *   Binary:         0b followed by binary digits (0-1)
        *   e.g.: 0b1010, 0B1101, 0b1110, etc.
    *   Octal:          0o followed by octal digits (0-7)
        *   e.g.: 0o12, 0O34, 0o56, etc.
*   Special Cases:
    *   Infinity:       inf or infinity
    *   Not a Number:   nan
*   Be sure to use the `IGNORECASE` flag when compiling this regex
*   Pattern
    *   `[+-]?`                     <br/>Sign
    *   Float or Integer
    *   `(?:...|...)`               <br/>Non-Capturing Option Group
        *   If Float or Base-10 Integer:
            *   `(?:...|...)`       <br/>Non-Capturing Option Group
                *   `\d+\.?\d*`     <br/>Integer or Float (trailing zero optional)
                *   `\.\d+`         <br/>Float (no leading zero)
                *   `(?:...)?`      <br/>Optional Non-Capturing Group
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
num_rgx = compile(f"^\s*({num_rgx_str})\s*$", flags=IGNORECASE)
r"""
### Number
*   Sign (optional + or -)
*   Basic Floats or Integer
    *   e.g.: 1, +2, -3, 0, +0, -0, 45, 6.0, +7.8, -9.0, 0.0, 0.1, 23., .45, etc.
*   Scientific Notation Supported
    *   e.g.: 0.0e+1, 1.0E-2, 2.3e4, 56E67, etc.
*   Non-Decimal Bases Supported:
    *   Hexadecimal:    0x followed by hex digits (0-9, a-f)
        *   e.g.: 0x1a, 0X2F, 0x3b, etc.
    *   Binary:         0b followed by binary digits (0-1)
        *   e.g.: 0b1010, 0B1101, 0b1110, etc.
    *   Octal:          0o followed by octal digits (0-7)
        *   e.g.: 0o12, 0O34, 0o56, etc.
*   Special Cases:
    *   Infinity:       inf or infinity
    *   Not a Number:   nan
*   Pattern: `^\s*([+-]?(?:(?:\d+\.?\d*|\.\d+)(?:e[+-]?\d+)?|0(?:x[\da-f]+|b[01]+|o[0-7]+)|inf(?:inity)?|nan))\s*$`
    *   `^`                             <br/>Start
    *   `\s*`                           <br/>Optional Whitespace
    0.  `(...)`                         <br/>Capture Group 0
        *   `[+-]?`                     <br/>Sign
        *   Float or Integer
        *   `(?:...|...)`               <br/>Non-Capturing Option Group
            *   If Float or Base-10 Integer:
                *   `(?:...|...)`       <br/>Non-Capturing Option Group
                    *   `\d+\.?\d*`     <br/>Integer or Float (trailing zero optional)
                    *   `\.\d+`         <br/>Float (no leading zero)
                    *   `(?:...)?`      <br/>Optional Non-Capturing Group
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

num_opl_rgx_str = rf"{num_rgx_str}(?<!\.)"
"""
### Number (leading zero optional)
*   Cannot end with a decimal point
*   Sign (optional + or -)
*   Float or Integer (leading zero optional)
*   Scientific Notation Not Supported
*   e.g.: 1, +2, -3, 0, +0, -0, 45, 6.0, +7.8, -9.0, 0.0, 0.1, .23, etc.
*   Be sure to use the `IGNORECASE` flag when compiling this regex
*   Pattern: `[+-]?(?:(?:\d+\.?\d*|\.\d+)(?:e[+-]?\d+)?|0(?:x[\da-f]+|b[01]+|o[0-7]+)|inf(?:inity)?|nan)(?<!\.)`
    *   `[+-]?`                     <br/>Sign
    *   Float or Integer
    *   `(?:...|...)`               <br/>Non-Capturing Option Group
        *   If Float or Base-10 Integer:
            *   `(?:...|...)`       <br/>Non-Capturing Option Group
                *   `\d+\.?\d*`     <br/>Integer or Float (trailing zero optional)
                *   `\.\d+`         <br/>Float (no leading zero)
                *   `(?:...)?`      <br/>Optional Non-Capturing Group
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
    *   `(?<!\.)`                   <br/>Cannot end with a decimal point
"""
num_opl_rgx = compile(f"^\s*({num_opl_rgx_str})\s*$", flags=IGNORECASE)
r"""
### Number (leading zero optional)
*   Cannot end with a decimal point
*   Sign (optional + or -)
*   Float or Integer (leading zero optional)
*   Scientific Notation Not Supported
*   e.g.: 1, +2, -3, 0, +0, -0, 45, 6.0, +7.8, -9.0, 0.0, 0.1, .23, etc.
*   Pattern: `^\s*([+-]?(?:(?:\d+\.?\d*|\.\d+)(?:e[+-]?\d+)?|0(?:x[\da-f]+|b[01]+|o[0-7]+)|inf(?:inity)?|nan)(?<!\.))\s*$`
    *   `^`                             <br/>Start
    *   `\s*`                           <br/>Optional Whitespace
    0.  `(...)`                         <br/>Capture Group 0
        *   `[+-]?`                     <br/>Sign
        *   Float or Integer
        *   `(?:...|...)`               <br/>Non-Capturing Option Group
            *   If Float or Base-10 Integer:
                *   `(?:...|...)`       <br/>Non-Capturing Option Group
                    *   `\d+\.?\d*`     <br/>Integer or Float (trailing zero optional)
                    *   `\.\d+`         <br/>Float (no leading zero)
                    *   `(?:...)?`      <br/>Optional Non-Capturing Group
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
        *   `(?<!\.)`                   <br/>Cannot end with a decimal point
    *   `\s*`                           <br/>Optional Whitespace
    *   `$`                             <br/>End
"""

num_opt_rgx_str = rf"(?!\.){num_rgx_str}"
"""
### Basic Number (trailing zero optional)
*   Cannot start with a decimal point
*   Sign (optional + or -)
*   Float or Integer (trailing zero optional)
*   Scientific Notation Not Supported
*   e.g.: 1, +2, -3, 0, +0, -0, 45, 6.0, +7.8, -9.0, 0.0, 0.1, 23., etc.
*   Be sure to use the `IGNORECASE` flag when compiling this regex
*   Pattern: `(?!\.)[+-]?(?:(?:\d+\.?\d*|\.\d+)(?:e[+-]?\d+)?|0(?:x[\da-f]+|b[01]+|o[0-7]+)|inf(?:inity)?|nan)`
    *   `(?!\.)`                    <br/>Cannot start with a decimal point
    *   `[+-]?`                     <br/>Sign
    *   Float or Integer
    *   `(?:...|...)`               <br/>Non-Capturing Option Group
        *   If Float or Base-10 Integer:
            *   `(?:...|...)`       <br/>Non-Capturing Option Group
                *   `\d+\.?\d*`     <br/>Integer or Float (trailing zero optional)
                *   `\.\d+`         <br/>Float (no leading zero)
                *   `(?:...)?`      <br/>Optional Non-Capturing Group
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
num_opt_rgx = compile(f"^\s*({num_opt_rgx_str})\s*$", flags=IGNORECASE)
r"""
### Basic Number (trailing zero optional)
*   Cannot start with a decimal point
*   Sign (optional + or -)
*   Float or Integer (trailing zero optional)
*   Scientific Notation Not Supported
*   e.g.: 1, +2, -3, 0, +0, -0, 45, 6.0, +7.8, -9.0, 0.0, 0.1, 23., etc.
*   Pattern: `(?!\.)[+-]?(?:(?:\d+\.?\d*|\.\d+)(?:e[+-]?\d+)?|0(?:x[\da-f]+|b[01]+|o[0-7]+)|inf(?:inity)?|nan)`
    *   `^`                             <br/>Start
    *   `\s*`                           <br/>Optional Whitespace
    0.  `(...)`                         <br/>Capture Group 0
        *   `(?!\.)`                    <br/>Cannot start with a decimal point
        *   `[+-]?`                     <br/>Sign
        *   Float or Integer
        *   `(?:...|...)`               <br/>Non-Capturing Option Group
            *   If Float or Base-10 Integer:
                *   `(?:...|...)`       <br/>Non-Capturing Option Group
                    *   `\d+\.?\d*`     <br/>Integer or Float (trailing zero optional)
                    *   `\.\d+`         <br/>Float (no leading zero)
                    *   `(?:...)?`      <br/>Optional Non-Capturing Group
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

### Scientific notation supported numbers ###

sci_rgx_str = r"[+-]?(?:\d+\.?\d*|\.\d+)e[+-]?\d+"
"""
### Scientific Notation Only
*   Sign (optional + or -)
*   e.g.: 0.0e+1, 1.0E-2, 2.3e4, 56E67, etc.
*   Be sure to use the `IGNORECASE` flag when compiling this regex
*   Pattern
    *   `[+-]?`         <br/>Sign
    *   Float or Integer
    *   `(?:...|...)`   <br/>Non-Capturing Option Group
        *   `\d+\.?\d*` <br/>Integer or Float (trailing zero optional)
        *   `\.\d+`     <br/>Float (no leading zero)
    *   `e[+-]?\d+`     <br/>Scientific Notation
"""
sci_rgx = compile(f"^\s*({sci_rgx_str})\s*$", flags=IGNORECASE)
r"""
### Scientific Notation Only
*   Sign (optional + or -)
*   e.g.: 0.0e+1, 1.0E-2, 2.3e4, 56E67, etc.
*   Pattern: `^\s*([+-]?(?:\d+\.?\d*|\.\d+)e[+-]?\d+)\s*$`
    *   `^`                 <br/>Start
    *   `\s*`               <br/>Optional Whitespace
    0.  `(...)`             <br/>Capture Group 0
        *   `[+-]?`         <br/>Sign
        *   `\d+(?:\.\d+)?` <br/>Integer or Float (significand)
        *   `[eE]`          <br/>Exponent Indicator
        *   `[+-]\d+`       <br/>Sign and exponent value
    *   `\s*`               <br/>Optional Whitespace
    *   `$`                 <br/>End
"""

def format_number(num: Number) -> str:
    """
    Format a number as a string with appropriate precision.
    
    Args:
        num (Union[int, float]): The number to format.
    
    Returns:
        str: The formatted number.
    """
    flt = float(num)
    # Use int if it’s an exact whole number
    # Otherwise, trim trailing zeros while keeping enough precision
    return str(int(flt)) if flt.is_integer() else f"{flt:.15g}"

def is_basic_float(num: str) -> bool:
    """
    Determine if a string represents a basic float number.
    
    Args:
        num (str): The string to check.
        
    Returns:
        bool: True if the string represents a basic float number, False otherwise.
    """
    return flt_bsc_rgx.match(num) is not None

def is_basic_int(num: str) -> bool:
    """
    Determine if a string represents a basic integer number.
    
    Args:
        num (str): The string to check.
        
    Returns:
        bool: True if the string represents a basic integer number, False otherwise.
    """
    return int_bsc_rgx.match(num) is not None

def is_float(num: str) -> bool:
    """
    Determine if a string represents a float number.
    
    Args:
        num (str): The string to check.
        
    Returns:
        bool: True if the string represents a float number, False otherwise.
    """
    return flt_rgx.match(num) is not None

def is_int(num: str) -> bool:
    """
    Determine if a string represents an integer number.
    
    Args:
        num (str): The string to check.
        
    Returns:
        bool: True if the string represents an integer number, False otherwise.
    """
    return int_rgx.match(num) is not None

def is_non_decimal(num: str) -> bool:
    """
    Determine if a string represents a non-decimal number (hex, binary, or octal).
    
    Args:
        num (str): The string to check.
        
    Returns:
        bool: True if the string represents a non-decimal number, False otherwise.
    """
    return int_bas_rgx.match(num) is not None

def is_number(num: str) -> bool:
    """
    Determine if a string represents a number (either int or float).
    
    Args:
        num (str): The string to check.
        
    Returns:
        bool: True if the string represents a number, False otherwise.
    """
    return num_rgx.match(num) is not None

def is_scinot(num: str) -> bool:
    """
    Determine if a string represents a scientific notation number.
    
    Args:
        num (str): The string to check.
        
    Returns:
        bool: True if the string represents a scientific notation number, False otherwise.
    """
    return sci_rgx.match(num) is not None

def to_number(num: str) -> Union[int, float]:
    """
    Convert a string to a number of the appropriate type (int or float) based on its format.

    Args:
        num (str): The string to convert.

    Returns:
        Union[int, float]: The converted number.
    """
    if int_rgx.match(num):
        return int(num)
    if flt_rgx.match(num):
        return float(num)
    
    raise ValueError(f"Invalid number format: {num}")