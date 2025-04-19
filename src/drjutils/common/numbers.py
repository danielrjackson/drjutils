"""
Number Utilities[+-]?

This module provides utilities for working with numbers (and strings that represent numbers).

Copyright 2025 Daniel Robert Jackson
"""

"""
Standard Libraries
"""
from numbers import Number
from re import compile, VERBOSE
from typing import Union

__all__ = [
    "flt_bsc_opl_rgx_str",
    "flt_bsc_opl_rgx",
    "flt_bsc_opt_rgx_str",
    "flt_bsc_opt_rgx",
    "flt_bsc_rgx_str",
    "flt_bsc_rgx",
    "flt_bsc_rlx_rgx_str",
    "flt_bsc_rlx_rgx",
    "flt_bsc_sct_rgx_str",
    "flt_bsc_sct_rgx",
    "flt_rgx_str",
    "flt_rgx",
    "flt_rlx_rgx_str",
    "flt_rlx_rgx",
    "flt_sct_rgx_str",
    "flt_sct_rgx",
    "format_number",
    "int_rgx_str",
    "int_rgx",
    "int_sct_rgx_str",
    "int_sct_rgx",
    "is_float",
    "is_int",
    "is_number",
    "num_bsc_opl_rgx_str",
    "num_bsc_opl_rgx",
    "num_bsc_opt_rgx_str",
    "num_bsc_opt_rgx",
    "num_bsc_rgx_str",
    "num_bsc_rgx",
    "num_bsc_rlx_rgx_str",
    "num_bsc_rlx_rgx",
    "num_bsc_sct_rgx_str",
    "num_bsc_sct_rgx",
    "num_opl_rgx_str",
    "num_opl_rgx",
    "num_opt_rgx_str",
    "num_opt_rgx",
    "num_rgx_str",
    "num_rgx",
    "num_rlx_rgx_str",
    "num_rlx_rgx",
    "num_sct_rgx_str",
    "num_sct_rgx",
    "sci_rgx_str",
    "sci_rgx",
    "sci_rlx_rgx_str",
    "sci_rlx_rgx",
    "sci_sct_rgx_str",
    "sci_sct_rgx",
    "sgn_opt_rgx_str",
    "sgn_req_rgx_str",
    "to_number"
]

### Floating point numbers ###

flt_bsc_opl_rgx_str = r"[+-]?(?:\d+\.\d+|\d*\.\d*[1-9]\d*)"
"""
### Basic Float (leading zero optional)
*   Sign (optional + or -)
*   Float Only (leading zero optional)
*   Scientific Notation Not Supported
*   e.g.:   1.0, +0.2, -34.56, .7, 0.0, +0.0, -0.0, etc.
*   Pattern
    *   `[+-]?`                 <br/>Sign (optional + or -)
    *   Float (leading zero optional)
    *   `(?:...|...)`           <br/>Non-Capturing Choice Group
        *   `\d+\.\d+`          <br/>Float
        *   `\d*\.\d*[1-9]\d*`  <br/>Float (leading digit optional; non-zero trailing digit)
"""
flt_bsc_opl_rgx = compile(f"^({flt_bsc_opl_rgx_str})$")
r"""
### Basic Float (leading zero optional)
*   Sign (optional + or -)
*   Float Only (leading zero optional)
*   Scientific Notation Not Supported
*   e.g.:   1.0, +0.2, -34.56, .7, etc.
*   Pattern: `^([+-]?(?:\d+\.\d+|\d*\.\d*[1-9]\d*))$`
    *   `^`             <br/>Start
    0.  `(...)`         <br/>Capture Group 0
        *   `[+-]?`                 <br/>Sign (optional + or -)
        *   Float (leading zero optional)
        *   `(?:...|...)`           <br/>Non-Capturing Choice Group
            *   `\d+\.\d+`          <br/>Float
            *   `\d*\.\d*[1-9]\d*`  <br/>Float (leading digit optional)
    *   `$`             <br/>End
"""

flt_bsc_opt_rgx_str = r"[+-]?\d+\.\d*"
"""
### Basic Float (trailing zero optional)
*   Sign (optional + or -)
*   Float Only (trailing zero optional)
*   Scientific Notation Not Supported
*   e.g.:   1.0, +0.2, -34.56, 7., etc.
*   Pattern
    *   `[+-]?`     <br/>Sign
    *   `\d+\.\d*`  <br/>Float
"""
flt_bsc_opt_rgx = compile(f"^({flt_bsc_opt_rgx_str})$")
r"""
### Basic Float (trailing zero optional)
*   Sign (optional + or -)
*   Float Only (trailing zero optional)
*   Scientific Notation Not Supported
*   e.g.:   1.0, +0.2, -34.56, 7., etc.
*   Pattern: `^([+-]?\d+\.\d*)$`
    *   `^`             <br/>Start
    0.  `(...)`         <br/>Capture Group 0
        *   `[+-]?`     <br/>Sign
        *   `\d+\.\d*`  <br/>Float
    *   `$`             <br/>End
"""

flt_bsc_rgx_str = r"[+-]?\d+\.\d+"
"""
### Basic Float
*   Sign (optional + or -)
*   Strict Complete Float Only
*   Scientific Notation Not Supported
*   e.g.:   1.0, +0.2, -34.56, etc.
*   Pattern
    *   `[+-]?`     <br/>Sign
    *   `\d+\.\d+`  <br/>Float
"""
flt_bsc_rgx = compile(f"^({flt_bsc_rgx_str})$")
r"""
### Basic Float
*   Sign (optional + or -)
*   Strict Complete Float Only
*   Scientific Notation Not Supported
*   e.g.:   1.0, +0.2, -34.56, etc.
*   Pattern: `^([+-]?\d+\.\d+)$`
    *   `^`             <br/>Start
    0.  `(...)`         <br/>Capture Group 0
        *   `[+-]?`     <br/>Sign
        *   `\d+\.\d+`  <br/>Float
    *   `$`             <br/>End
"""

flt_bsc_rlx_rgx_str = r"[+-]?(?:\d+\.\d*|\d*\.\d*[1-9]\d*)"
"""
### Basic Float (Relaxed)
*   Sign (optional + or -)
*   Relaxed Float Only (optional leading or trailing zero)
*   Scientific Notation Not Supported
*   e.g.:   1.0, +0.2, -34.56, 7., .89, etc.
*   Pattern
    *   `[+-]?`                 <br/>Sign
    *   Relaxed Float
    *   `(?:...|...)`           <br/>Non-Capturing Choice Group
        *   `\d+\.\d*`          <br/>Float (trailing zero optional)
        *   `\d*\.\d*[1-9]\d*`  <br/>Float (leading zero optional)
"""
flt_bsc_rlx_rgx = compile(f"^({flt_bsc_rlx_rgx_str})$")
r"""
### Basic Float (Relaxed)
*   Sign (optional + or -)
*   Relaxed Float Only (optional leading or trailing zero)
*   Scientific Notation Not Supported
*   e.g.:   1.0, +0.2, -34.56, 7., .89, etc.
*   Pattern: `^([+-]?(?:\d+\.\d*|\d*\.\d*[1-9]\d*))$`
    *   `^`                         <br/>Start
    0.  `(...)`                     <br/>Capture Group 0
        *   `[+-]?`                 <br/>Sign
        *   Relaxed Float
        *   `(?:...|...)`           <br/>Non-Capturing Choice Group
            *   `\d+\.\d*`          <br/>Float (trailing zero optional)
            *   `\d*\.\d*[1-9]\d*`  <br/>Float (leading zero optional)
    *   `$`                         <br/>End
"""

flt_bsc_sct_rgx_str = r"\d+\.\d+|-\d+\.\d*[1-9]\d*|-\d*[1-9]\d*\.\d+"
"""
### Basic Float (Strict)
*   Sign (optional -)
*   Strict Complete Float Only
*   Scientific Notation Not Supported
*   e.g.:   1.0, 0.2, -34.56, etc.
*   Pattern
    *   If Non-Negative Float:
        *   `\d+\.\d+`  <br/>Float
    *   If Negative Float:
        *   `-\d+\.\d*[1-9]\d*`  <br/>Negative Float (non-zero trailing digit)
        *   `-\d*[1-9]\d*\.\d+`  <br/>Negative Float (non-zero leading digit)
"""
flt_bsc_sct_rgx = compile(f"^({flt_bsc_sct_rgx_str})$")
r"""
### Basic Float (Strict)
*   Sign (optional -)
*   Strict Complete Float Only
*   Scientific Notation Not Supported
*   e.g.:   1.0, 0.2, -34.56, etc.
*   Pattern: `^(\d+\.\d+|-\d+\.\d*[1-9]\d*|-\d*[1-9]\d*\.\d+)$`
    *   `^`             <br/>Start
    0.  `(...)`         <br/>Capture Group 0
        *   If Non-Negative Float:
            *   `\d+\.\d+`  <br/>Float
        *   If Negative Float:
            *   `-\d+\.\d*[1-9]\d*`  <br/>Negative Float (non-zero trailing digit)
            *   `-\d*[1-9]\d*\.\d+`  <br/>Negative Float (non-zero leading digit)
    *   `$`             <br/>End
"""

flt_rgx_str = r"[+-]?(?:\d+\.\d+|[1-9](?:\.\d+)?[eE](?:+?\d+|-[1-9]\d*))"
"""
### Float Number
*   Sign (optional + or -)
*   Strict Complete Float Only
*   Scientific Notation Supported
    *   Significand:    non-zero digit followed by optional decimal and digits
    *   Exponent:       e or E followed by optional sign (+ or -) and required int digits
*   e.g.:   1.0, +0.2, -34.56, 7.8e+0, -9.0e-1, 2.3e4, etc.
*   Pattern
    *   `[+-]?`                     <br/>Sign
    *   Float or Scientific Notation
    *   `(?:...|...)`               <br/>Non-Capturing Choice Group
        *   If not SciNot:
            *   `\d+\.\d+`          <br/>Float
        *   If SciNot:
            *   `[1-9](?:\.\d+)?`   <br/>Significand
            *   `[eE]`              <br/>Exponent
            *   (?:...|...)`        <br/>Non-Capturing Choice Group
                *   `+?\d+`         <br/>Positive Exponent (optional +)
                *   `-[1-9]\d*`     <br/>Negative Exponent
"""
flt_rgx = compile(f"^({flt_rgx_str})$")
r"""
### Float Number
*   Sign (optional + or -)
*   Strict Complete Float Only
*   Scientific Notation Supported
    *   Significand:    non-zero digit followed by optional decimal and digits
    *   Exponent:       e or E followed by optional sign (+ or -) and required int digits
*   e.g.:   1.0, +0.2, -34.56, 7.8e+0, -9.0e-1, 2.3e4, etc.
*   Pattern: `^([+-]?(?:\d+\.\d+|[1-9](?:\.\d+)?[eE](?:+?\d+|-[1-9]\d*)))$`
    *   `^`                             <br/>Start
    0.  `(...)`                         <br/>Capture Group 0
        *   `[+-]?`                     <br/>Sign
        *   Float or Scientific Notation
        *   `(?:...|...)`               <br/>Non-Capturing Choice Group
            *   If Float:
                *   `\d+\.\d+`          <br/>Float
            *   If SciNot:
                *   `[1-9](?:\.\d+)?`   <br/>Significand
                *   `[eE]`              <br/>Exponent
                *   (?:...|...)`        <br/>Non-Capturing Choice Group
                    *   `+?\d+`         <br/>Positive Exponent (optional +)
                    *   `-[1-9]\d*`     <br/>Negative Exponent
    *   `$`                             <br/>End
"""

flt_rlx_rgx_str = r"[+-]?(?:\d+\.\d*|\d*\.\d*[1-9]\d*|(?:\d*[1-9]\d*\.\d*|\d*\.\d*[1-9]\d*)[eE][+-]?\d+)"
"""
### Float Number (Relaxed)
*   Sign (optional + or -)
*   Relaxed Float Only (optional leading or trailing zero)
*   Scientific Notation Supported
    *   Significand:    relaxed float or int (optional decimal)
    *   Exponent:       e or E followed by optional sign (+ or -) and required int digits
*   e.g.:   1.0, +0.2, -34.56, 7., .89, 0.1e-0, -2.3e45, 6e8, 9.e+0, .1e-23, etc.
*   Pattern
    *   `[+-]?`                         <br/>Sign
    *   Relaxed Float or Scientific Notation
    *   `(?:...|...)`                   <br/>Non-Capturing Choice Group
        *   If Float:
            *   Relaxed Float
            *   `\d+\.\d*`              <br/>Float (trailing optional)
            *   `\d*\.\d*[1-9]\d*`      <br/>Float (leading optional)
        *   If SciNot:
            *   `(?:...|...)`           <br/>Non-Capturing Choice Group
                *   Significand
                *   `\d*[1-9]\d*\.\d*`  <br/>Non-Zero Leading Float (trailing optional)
                *   `\d*\.\d*[1-9]\d*`  <br/>Non-Zero Trailing Float (leading optional)
            *   `[eE][+-]?\d+`          <br/>Exponent
"""
flt_rlx_rgx = compile(f"^({flt_rlx_rgx_str})$")
r"""
### Float Number (Relaxed)
*   Sign (optional + or -)
*   Relaxed Float Only (optional leading or trailing zero)
*   Scientific Notation Supported
    *   Significand:    relaxed float or int (optional decimal)
    *   Exponent:       e or E followed by optional sign (+ or -) and required int digits
*   e.g.:   1.0, +0.2, -34.56, 7., .89, 0.1e-0, -2.3e45, 6e8, 9.e+0, .1e-23, etc.
*   Pattern: `^([+-]?(?:\d+\.\d*|\d*\.\d*[1-9]\d*|(?:\d*[1-9]\d*\.\d*|\d*\.\d*[1-9]\d*)[eE][+-]?\d+))$`
    *   `^`                                 <br/>Start
    0.  `(...)`                             <br/>Capture Group 0
        *   `[+-]?`                         <br/>Sign
        *   Relaxed Float or Scientific Notation
        *   `(?:...|...)`                   <br/>Non-Capturing Choice Group
            *   If Float:
                *   Relaxed Float
                *   `\d+\.\d*`              <br/>Float (trailing optional)
                *   `\d*\.\d*[1-9]\d*`      <br/>Float (leading optional)
            *   If SciNot:
                *   `(?:...|...)`           <br/>Non-Capturing Choice Group
                    *   Significand
                    *   `\d*[1-9]\d*\.\d*`  <br/>Non-Zero Leading Float (trailing optional)
                    *   `\d*\.\d*[1-9]\d*`  <br/>Non-Zero Trailing Float (leading optional)
                *   `[eE][+-]?\d+`          <br/>Exponent
    *   `$`                                 <br/>End
"""

flt_sct_rgx_str = r"-?\d+\.\d+|-?(?:\d*[1-9]\d*\.\d+|\d+\.\d*[1-9]\d*)e(?:+\d+|-[1-9]\d*)"
"""
### Float Number (Strict)
*   Sign (optional -)
*   Strict Complete Float Only
*   Scientific Notation Supported
    *   Significand:    non-zero digit followed by decimal and digits
    *   Exponent:       e followed by sign (+ or -) and int digits
*   e.g.:   1.0, 0.0, -2.3, 34.56, 7.8e+0, -9.0e-1, etc.
*   Pattern
    *   If Float:
        *   `-?\d+\.\d+`            <br/>Float
    *   If SciNot:
        *   Significand
        *   `-?`                    <br/>Sign
        *   `(?:...|...)`           <br/>Non-Capturing Choice Group
            *   `\d*[1-9]\d*\.\d+`  <br/>Non-Zero Leading Float
            *   `\d+\.\d*[1-9]\d*`  <br/>Non-Zero Trailing Float
        *   `e`                     <br/>Exponent
        *   `(?:...|...)`           <br/>Non-Capturing Choice Group
            *   `+\d+`              <br/>Positive Exponent
            *   `-[1-9]\d*`         <br/>Non-Zero Negative Exponent
"""
flt_sct_rgx = compile(f"^({flt_sct_rgx_str})$")
r"""
### Float Number (Strict)
*   Sign (optional -)
*   Strict Complete Float Only
*   Scientific Notation Supported
    *   Significand:    non-zero digit followed by decimal and digits
    *   Exponent:       e followed by sign (+ or -) and int digits
*   e.g.:   1.0, 0.0, -2.3, 34.56, 7.8e+0, -9.0e-1, etc.
*   Pattern: `^(-?\d+\.\d+|-?(?:\d*[1-9]\d*\.\d+|\d+\.\d*[1-9]\d*)e(?:+\d+|-[1-9]\d*))$`
    *   `^`                             <br/>Start
    0.  `(...)`                         <br/>Capture Group 0
        *   If Float:
            *   `-?\d+\.\d+`            <br/>Float
        *   If SciNot:
            *   Significand
            *   `-?`                    <br/>Sign
            *   `(?:...|...)`           <br/>Non-Capturing Choice Group
                *   `\d*[1-9]\d*\.\d+`  <br/>Non-Zero Leading Float
                *   `\d+\.\d*[1-9]\d*`  <br/>Non-Zero Trailing Float
            *   `e`                     <br/>Exponent
            *   `(?:...|...)`           <br/>Non-Capturing Choice Group
                *   `+\d+`              <br/>Positive Exponent
                *   `-[1-9]\d*`         <br/>Non-Zero Negative Exponent
    *   `$`                             <br/>End
"""

### Integers ###

int_rgx_str = rf"[+-]?\d+"
"""
### Integer Number
*   Sign (optional + or -)
*   Integer Only
*   e.g.:   1, +2, -3, +0, -0, 42, etc.
*   Pattern
    *   `[+-]?`      <br/>Sign
    *   `\d+`        <br/>Integer
"""
int_rgx = compile(f"^({int_rgx_str})$")
r"""
### Integer Number
*   Sign (optional + or -)
*   Integer Only
*   e.g.:   1, +2, -3, +0, -0, 42, etc.
*   Pattern: `^([+-]?\d+)$`
    *   `^`         <br/>Start
    0.  `(...)`     <br/>Capture Group 0
        *   `[+-]?`      <br/>Sign
        *   `\d+`        <br/>Integer
    *   `$`         <br/>End
"""

int_sct_rgx_str = rf"\d+|-\d*[1-9]\d*"
"""
### Integer Number (Strict)
*   Sign (optional -)
*   Integer Only
*   e.g.:   0, 1, -2, 42, etc.
*   Pattern
    *   If Non-Negative Integer:
        *   `\d+`           <br/>Integer
    *   If Negative Integer:
        *   `-\d*[1-9]\d*`  <br/>Negative Integer
"""
int_sct_rgx = compile(f"^({int_sct_rgx_str})$")
r"""
### Integer Number (Strict)
*   Sign (optional -)
*   Integer Only
*   e.g.:   0, 1, -2, 42, etc.
*   Pattern: `^(\d+|-\d*[1-9]\d*)$`
    *   `^`                     <br/>Start
    0.  `(...)`                 <br/>Capture Group 0
        *   If Non-Negative Integer:
            *   `\d+`           <br/>Integer
        *   If Negative Integer:
            *   `-\d*[1-9]\d*`  <br/>Negative Integer
    *   `$`                     <br/>End
"""

### Generic Numbers (Floats or Ints) ###

num_bsc_opl_rgx_str = r"[+-]?(?:\d+|\d+\.\d+|\d*\.\d*[1-9]\d*)"
"""
### Basic Number (leading zero optional)
*   Sign (optional + or -)
*   Float or Integer (leading zero optional)
*   Scientific Notation Not Supported
*   e.g.:  1, +2, -3, 0, +0, -0, 45, 6.0, +7.8, -9.0, 0.0, 0.1, .23, etc.
*   Pattern
    *   `[+-]?`                 <br/>Sign
    *   Float or Integer
    *   `(?:...|...)`           <br/>Non-Capturing Choice Group
        *   `\d+`               <br/>Integer
        *   `\d+\.\d+`          <br/>Float
        *   `\d*\.\d*[1-9]\d*`  <br/>Non-Zero Trailing Float (leading digit optional)
"""
num_bsc_opl_rgx = compile(f"^({num_bsc_opl_rgx_str})$")
r"""
### Basic Number (leading zero optional)
*   Sign (optional + or -)
*   Float or Integer (leading zero optional)
*   Scientific Notation Not Supported
*   e.g.:  1, +2, -3, 0, +0, -0, 45, 6.0, +7.8, -9.0, 0.0, 0.1, .23, etc.
*   Pattern: `^([+-]?(?:\d+|\d+\.\d+|\d*\.\d*[1-9]\d*))$`
    *   `^`                         <br/>Start
    0.  `(...)`                     <br/>Capture Group 0
        *   `[+-]?`                 <br/>Sign
        *   Float or Integer
        *   `(?:...|...)`           <br/>Non-Capturing Choice Group
            *   `\d+`               <br/>Integer
            *   `\d+\.\d+`          <br/>Float
            *   `\d*\.\d*[1-9]\d*`  <br/>Non-Zero Trailing Float (leading digit optional)
    *   `$`                         <br/>End
"""

num_bsc_opt_rgx_str = r"[+-]?\d+\.?\d*"
"""
### Basic Number
*   Sign (optional + or -)
*   Float or Integer (trailing zero optional)
*   Scientific Notation Not Supported
*   e.g.:  1, +2, -3, 0, +0, -0, 45, 6.0, +7.8, -9.0, 0.0, 0.1, 23., etc.
*   Pattern
    *   `[+-]?`         <br/>Sign
    *   Float or Integer
        *   `\d+`       <br/>Integer
        *   `\.?\d*`    <br/>Trailing Zero Optional Float
"""
num_bsc_opt_rgx = compile(f"^({num_bsc_opt_rgx_str})$")
r"""
### Basic Number
*   Sign (optional + or -)
*   Float or Integer (trailing zero optional)
*   Scientific Notation Not Supported
*   e.g.:  1, +2, -3, 0, +0, -0, 45, 6.0, +7.8, -9.0, 0.0, 0.1, 23., etc.
*   Pattern: `^([+-]?\d+\.?\d*)$`
    *   `^`             <br/>Start
    0.  `(...)`         <br/>Capture Group 0
        *   `[+-]?`         <br/>Sign
        *   Float or Integer
            *   `\d+`       <br/>Integer
            *   `\.?\d*`    <br/>Trailing Zero Optional Float
    *   `$`             <br/>End
"""

num_bsc_rgx_str = r"[+-]?\d+(?:\.\d+)?"
"""
### Basic Number
*   Sign (optional + or -)
*   Float or Integer
*   Scientific Notation Not Supported
*   Pattern
    *   `[+-]?`      <br/>Sign
        *   <br/>Float
    *   integers valid: decimal optional
"""
num_bsc_rgx = compile(f"^({num_bsc_rgx_str})$")
r"""
### Basic Number
*   Sign (optional + or -)
Pattern: `^([+-]?\d+(?:\.\d+)?)$`
    *   `[+-]?`      <br/>Sign
        *   <br/>Float
    *   integers valid: decimal optional
*   e.g.:   1.0, +0.1, -2.5, 42, etc.
"""

num_bsc_rlx_rgx_str = r"[+-]?(?:\d*\.?\d+|\d+\.\d*)"
"""
### Basic Number
*   Sign (optional + or -)
*   e.g.:   1.0, +1., .0, 0., -1, 0, etc.
*   Pattern
*   Sign optional:  + or -
*   Relaxed floats: leading or trailing zeros optional
*   integers valid: decimal optional
"""
num_bsc_rlx_rgx = compile(f"^({num_bsc_rlx_rgx_str})$")
r"""
### Basic Number
*   Sign (optional + or -)
Pattern: `^([+-]?(?:\d*\.?\d+|\d+\.\d*))$`
*   Sign optional:  + or -
*   Relaxed floats: leading or trailing zeros optional
*   integers valid: decimal optional
*   e.g.:   1.0, +1., .0, 0., -1, 0, etc.
"""

num_bsc_sct_rgx_str = r"-?\d+(?:\.\d+)?"
"""
### Basic Number
*   Sign (optional + or -)
*   e.g.:   1.0, 0.1, -2.5, 42, etc.
*   Pattern
    *   `-?`      <br/>Sign optional (- only)
        *   <br/>Float
    *   integers valid: decimal optional
"""
num_bsc_sct_rgx = compile(f"^({num_bsc_sct_rgx_str})$")
r"""
### Basic Number
*   Sign (optional + or -)
*   e.g.:   1.0, 0.1, -2.5, 42, etc.
*   Pattern: `^(-?\d+(?:\.\d+)?)$`
    *   `-?`      <br/>Sign optional (- only)
        *   <br/>Float
    *   integers valid: decimal optional
"""

num_opl_rgx_str = r"[+-]?\d*\.?\d+(?:[eE][+-]?\d+)?"
"""
### Numbers
*   Sign (optional + or -)
*   e.g.:   +1.0, -2, .3, 0.4, 5.0e+6, 7e-8, -.9E+2, etc.
*   Pattern
    *   `[+-]?`      <br/>Sign
        *   <br/>Relaxed floats: leading zero optional
    *   integers valid: decimal optional        <br/>SciNot:      e or E followed by optional + or - sign and required int digits
"""
num_opl_rgx = compile(f"^({num_opl_rgx_str})$")
r"""
### Numbers
*   Sign (optional + or -)
*   e.g.:   +1.0, -2, .3, 0.4, 5.0e+6, 7e-8, -.9E+2, etc.
*   Pattern: `^([+-]?\d*\.?\d+(?:[eE][+-]?\d+)?)`
    *   `[+-]?`      <br/>Sign
        *   <br/>Relaxed floats: leading zero optional
    *   integers valid: decimal optional        <br/>SciNot:      e or E followed by optional + or - sign and required int digits
"""

num_opt_rgx_str = r"[+-]?\d+\.?\d*(?:[eE][+-]?\d+)?"
"""
### Numbers
*   Sign (optional + or -)
*   e.g.:   +1.0, -2, 0.3, 4., 5.0e+6, 7e-8, -9.E+2, etc.
*   Pattern
    *   `[+-]?`      <br/>Sign
        *   <br/>Relaxed floats: trailing zero optional
    *   integers valid: decimal optional        <br/>SciNot:      e or E followed by optional + or - sign and required int digits
"""
num_opt_rgx = compile(f"^({num_opt_rgx_str})$")
r"""
### Numbers
*   Sign (optional + or -)
*   e.g.:   +1.0, -2, 0.3, 4., 5.0e+6, 7e-8, -9.E+2, etc.
*   Pattern: `^([+-]?\d+\.?\d*(?:[eE][+-]?\d+)?)$`
    *   `[+-]?`      <br/>Sign
        *   <br/>Relaxed floats: trailing zero optional
    *   integers valid: decimal optional        <br/>SciNot:      e or E followed by optional + or - sign and required int digits
"""

num_rgx_str = r"[+-]?(?:\d+(?:\.\d+)?|[1-9](?:\.\d+)?[eE][+-]\d+)"
"""
### Numbers
*   Sign (optional + or -)
*   e.g.:   +1.0, -2, 0.3, 4.0, 5.0e+6, -0.7e-8, etc.
*   Pattern
    *   `[+-]?`      <br/>Sign
        *   <br/>Float
    *   integers valid: decimal optional        <br/>SciNot:      e or E followed by + or - sign and int digits
"""
num_rgx = compile(f"^({num_rgx_str})$")
r"""
### Numbers
*   Sign (optional + or -)
*   e.g.:   +1.0, -2, 0.3, 4.0, 5.0e+6, -0.7e-8, etc.
*   Pattern: `^([+-]?(?:\d+(?:\.\d+)?|[1-9](?:\.\d+)?[eE][+-]\d+))$`
    *   `[+-]?`      <br/>Sign
        *   <br/>Float
    *   integers valid: decimal optional        <br/>SciNot:      e or E followed by + or - sign and int digits
"""

num_rlx_rgx_str = r"[+-]?(?:\d*\.?\d+|\d+\.\d*)(?:[eE][+-]?\d+)?"
"""
### Numbers
*   Sign (optional + or -)
*   e.g.:   1.0, 0.3, -2.5, 4., 5.0e+6, 7e-8, etc.
*   Pattern
    * sign optional:  + or -
    * relaxed float (leading or trailing zero optional)
    * integers valid: decimal optional (not with SciNot)
    * SciNot:      e or E followed by optional + or - sign and required int digits
* e.g.:   +1.0, -2, .3, 0.4, 5., 6.0e+7, 8e-9, -.1e2, 345.E-6, etc.
"""
num_rlx_rgx = compile(f"^({num_rlx_rgx_str})$")
r"""
### Numbers
*   Sign (optional + or -)
*   Pattern: `^([+-]?(?:\d*\.?\d+|\d+\.\d*)(?:[eE][+-]?\d+)?)$`
    *   `[+-]?`      <br/>Sign
        *   <br/>Relaxed float (leading or trailing zero optional)
    *   integers valid: decimal optional (not with SciNot)        <br/>SciNot:      e or E followed by optional + or - sign and required int digits
* e.g.:   +1.0, -2, .3, 0.4, 5., 6.0e+7, 8e-9, -.1e2, 345.E-6, etc.
"""

num_sct_rgx_str = r"-?(?:\d+(?:\.\d+)?|[1-9]\.\d+e[+-]\d+)"
"""
### Numbers
*   Sign (optional + or -)
*   Pattern
    *   `-?`      <br/>Sign optional (- only)
        *   <br/>Float
    *   integers valid: decimal optional        <br/>SciNot:      e followed by + or - sign and int digits
"""
num_sct_rgx = compile(f"^({num_sct_rgx_str})$")
r"""
### Numbers
*   Sign (optional + or -)
*   e.g.:   1.0, 0.3, -2.5, 4., 5.0e+6, 7e-8, etc.
*   Pattern: `^(-?(?:\d+(?:\.\d+)?|[1-9]\.\d+e[+-]\d+))$`
    *   `-?`      <br/>Sign optional (- only)
        *   <br/>Float
    *   integers valid: decimal optional        <br/>SciNot:      e followed by required + or - sign and int digits
"""

### Scientific notation supported numbers ###

sci_rgx_str = r"[+-]?\d+(?:\.\d+)?[eE][+-]\d+"
"""
### Scientific Notation Only
*   Sign (optional + or -)
*   e.g.:   1e+2, +3.0e-4, -5.6E+3, etc.
*   Pattern        <br/>Floats:  floats require leading and trailing zeros
    *   integers valid: decimal optional
    *   `[+-]?`      <br/>Sign
        *   <br/>SciNot:      e or E followed by + or - sign and int digits
"""
sci_rgx = compile(f"^({sci_rgx_str})$")
r"""
### Scientific Notation Only
*   Sign (optional + or -)
*   e.g.:   1e+2, +3.0e-4, -5.6E+3, etc.
*   Pattern: `^([+-]?\d+(?:\.\d+)?[eE][+-]\d+)$`
    *   `[+-]?`      <br/>Sign
        *   <br/>Floats:  floats require leading and trailing zeros
    *   integers valid: decimal optional        <br/>SciNot:      e or E followed by + or - sign and int digits
"""

sci_rlx_rgx_str = r"[+-]?(?:\d*\.?\d+|\d+\.\d*)[eE][+-]?\d+"
"""
### Scientific Notation Only
*   Sign (optional + or -)
*   e.g.:   1e+2, +3.0e-4, -.5e6, 7.E8, etc.
*   Pattern
    *   `[+-]?`      <br/>Sign
        *   <br/>Relaxed float (leading or trailing zero optional)
    *   integers valid: decimal optional        <br/>SciNot:      e or E followed by optional + or - sign and required int digits
"""
sci_rlx_rgx = compile(f"^({sci_rlx_rgx_str})$")
r"""
### Scientific Notation Only
*   Sign (optional + or -)
*   e.g.:   1e+2, +3.0e-4, -.5e6, 7.E8, etc.
*   Pattern: `^([+-]?(?:\d*\.?\d+|\d+\.\d*)[eE][+-]?\d+)$`
    *   `[+-]?`      <br/>Sign
        *   <br/>Relaxed float (leading or trailing zero optional)
    *   integers valid: decimal optional        <br/>SciNot:      e or E followed by optional + or - sign and required int digits
"""

sci_sct_rgx_str = r"-?\d+(?:\.\d+)?e[+-]\d+"
"""
### Scientific Notation Only
*   Sign (optional + or -)
*   e.g.:   1e+2, 0.3e-4, -5.6e+7, 8.0e-9, etc.
*   Pattern
    *   `-?`      <br/>Sign optional (- only)
        *   <br/>Floats:  floats require leading and trailing zeros
    *   integers valid: decimal optional        <br/>SciNot:      e followed by required + or - sign and int digits
"""
sci_sct_rgx = compile(f"^({sci_sct_rgx_str})$")
r"""
### Scientific Notation Only
*   Sign (optional + or -)
*   e.g.:   1e+2, 0.3e-4, -5.6e+7, 8.0e-9, etc.
*   Pattern: `^(-?\d+(?:\.\d+)?e[+-]\d+)$`
    *   `-?`      <br/>Sign optional (- only)
        *   <br/>Floats:  floats require leading and trailing zeros
    *   integers valid: decimal optional        <br/>SciNot:      e followed by required + or - sign and int digits
"""

# Signs

sgn_opt_rgx_str = r"[+-]?"
"""
### Number Sign Regex String (Optional)
*   Sign (optional + or -)
*   Pattern
    *   Optional sign (+ or -) for numbers.
"""

sgn_req_rgx_str = r"[+-]"
"""
### Number Sign Regex String
*   Sign (optional + or -)
*   Pattern
    *   Required sign (+ or -) for numbers.
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

def is_number(num: str) -> bool:
    """
    Determine if a string represents a number (either int or float).
    
    Args:
        num (str): The string to check.
        
    Returns:
        bool: True if the string represents a number, False otherwise.
    """
    return num_rgx.match(num) is not None

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