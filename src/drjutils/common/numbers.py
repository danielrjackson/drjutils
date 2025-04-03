"""
Number Utilities

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
    "flt_bsc_rgx",
    "flt_bsc_rgx_str",
    "flt_rgx",
    "flt_rgx_str",
    "format_number",
    "int_rgx",
    "int_rgx_str",
    "is_float",
    "is_int",
    "is_number",
    "led_dec_opt_rgx_str",
    "led_dec_req_rgx_str",
    "num_bsc_rgx",
    "num_bsc_rgx_str",
    "num_rgx",
    "num_rgx_str",
    "sci_rgx",
    "sci_rgx_str",
    "sgn_opt_rgx_str",
    "strct_flt_rgx_str",
    "strct_num_rgx",
    "strct_num_rgx_str",
    "to_number",
    "trl_dec_opt_rgx_str",
    "trl_dec_req_rgx_str"
]


# Signs
sgn_opt_rgx_str = r"[+-]?"


# Integer number
# e.g. +1, -1, 0, 42, etc.
int_rgx_str    = f"[+-]?\d+"
int_rgx        = compile(f"^({int_rgx_str})$")

# Float numbers

# Leading decimal and zero optional (integer valid)
# e.g. 1.0, +0.1, -1.5, .0, 6, etc.
led_dec_opt_rgx_str = r"[+-]?\d*\.?\d+"
# Leading decimal required, leading zero optional (not integer)
# e.g. 1.0, +0.1, -1.5, .0, etc.
led_dec_req_rgx_str = r"[+-]?\d*\.\d+"
# Trailing decimal and zero optional (integer valid)
# e.g. 1.0, +1., 0., -5, etc.
trl_dec_opt_rgx_str = r"[+-]?\d+\.?\d*"
# Trailing decimal required, trailing zero optional (not integer)
# e.g. 1.0, +1., 0., -3., etc.
trl_dec_req_rgx_str = r"[+-]?\d+\.\d*"
# Strict float (must have number before and after decimal)
# e.g. 1.0, +0.1, -2.5, etc.
strct_flt_rgx_str   = r"[+-]?\d+\.\d+"
# Basic number (leading/trailing zeros and decimal optional, integers valid)
# e.g. 1.0, +1., .0, 0., -1, 0, etc.
num_bsc_rgx_str     = r"[+-]?(?:\d*\.?\d+|\d+\.\d*)"
num_bsc_rgx         = compile(f"^({num_bsc_rgx_str})$")

# Basic float with decimal, but optional leading/trailing zero (not integer)
# e.g. 1.0, 1., .0, 0., 0.1, 1.5, etc.
flt_bsc_rgx_str     = r"[+-]?(?:\d*\.\d+|\d+\.\d*)"
flt_bsc_rgx         = compile(f"^({flt_bsc_rgx_str})$")

# Scientific notation float
# e.g. 1e-5, +1.5e+5, -.2e3, etc.
sci_rgx_str         = r"[+-]?(?:\d*\.?\d+|\d+\.\d*)[eE][+-]?\d+"
sci_rgx             = compile(f"^({sci_rgx_str})$")

# e.g. +1.0, -1., .1, 0.1, 1e-5, 1.5e+5, etc.
flt_rgx_str         = r"[+-]?(?:\d*\.\d+|\d+\.\d*|(?:\d*\.?\d+|\d+\.\d*)[eE][+-]?\d+)"
flt_rgx             = compile(f"^({flt_rgx_str})$")

# Integer or float number
num_rgx_str         = r"[+-]?(?:\d*\.?\d+|\d+\.\d*)(?:[eE][+-]?\d+)?"
num_rgx             = compile(f"^({num_rgx_str})$")

strct_num_rgx_str   = r"-?\d+(?:\.\d+)(?:e[+-]\d+)?"
strct_num_rgx       = compile(f"^({strct_num_rgx_str})$")

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