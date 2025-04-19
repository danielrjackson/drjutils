"""
Interval helper functions for working with ranges of numbers.

This module provides helper functions for working with ranges of numbers.

Copyright 2025 Daniel Robert Jackson
"""

"""
Standard Libraries
"""
from re     import compile, Match, VERBOSE
from typing import Tuple, Union

"""
External Libraries
"""
from sympy import Interval

"""
Internal Libraries
"""
from .numbers import format_number, num_opl_rgx_str, num_opt_rgx_str, num_sct_rgx_str, num_rlx_rgx_str, to_number

__all__ = [
    "check_interval_str_match",
    "check_std_interval_str_match",
    "check_valid_interval_values",
    "format_interval",
    "interval_rgx",
    "interval_rgx_str",
    "is_float_interval",
    "is_int_interval",
    "is_interval_str",
    "is_std_interval_str",
    "std_interval_rgx",
    "std_interval_rgx_str",
    "to_interval",
    "to_std_interval_str"
]
_invl_rlx_spc_rgx_str = rf"({num_opl_rgx_str})\.\.({num_opt_rgx_str})"
_invl_sct_spc_rgx_str = rf"({num_rlx_rgx_str})\s+\.\.\s+({num_rlx_rgx_str})"
interval_rgx_str = rf"([\[(])?\s*(?:{_invl_rlx_spc_rgx_str}|{_invl_sct_spc_rgx_str})\s*([\])])?"
r"""
# String that can be used as a regex that matches interval strings (permissive formatting)
* Note that in this regex:
    *   we can't allow a trailing decimal after the minimum value,
    *   or a leading decimal before the maximum value
    *   unless there are spaces between the numbers and the ellipsis
    *   because it would be ambiguous with the ellipsis separator.
*   Pattern:
    *   0:  ([\[(])?
        *   Optional left bracket or parenthesis ('[':inclusive|'(':exclusive)
    *   \s*(?:          (not captured)
    *   If no spaces around the ellipsis
        *   1:  ([+-]?\\d*\\.?\\d+(?:[eE][+-]?\\d+)?)
            *   Minimum value (can be float or int)
            *   Cannot end with a decimal (e.g. "1." is not valid)
        *   \.\.        (not captured)
        *   2:  ([+-]?\\d+\\.?\\d*(?:[eE][+-]?\\d+)?)    
            *   Maximum value (can be float or int)
            *   Cannot start with a decimal (e.g. ".2" is not valid)
    *   If spaces around the ellipsis
        *   3:  ([+-]?(?:\\d*\\.?\\d+|\\d+\\.\\d*)(?:[eE][+-]?\\d+)?)
            *   Minimum value (can be float or int)
            *   Any valid number works here (e.g. "1.", ".2", "1e-5", etc.)
        *   \s+\.\.\s+  (not captured)
        *   4:  ([+-]?(?:\\d*\\.?\\d+|\\d+\\.\\d*)(?:[eE][+-]?\\d+)?)
            *   Maximum value (can be float or int)
            *   Any valid number works here (e.g. "1.", ".2", "1e-5", etc.)
    *   )\s*            (not captured)
    *   5:  ([\])])?
        *   Optional right bracket or parenthesis (']':inclusive|')':exclusive)
*   e.g.:   "[ 1 .. 2 ]", "(1 .. 2)", "[1..2)", "(1..2]", "1..2", "1e-5..2e+5", etc.
"""

interval_rgx = compile(f"^\s*{interval_rgx_str}\s*$")
r"""
# Regex pattern that matches interval strings (permissive formatting)
* Note that in this regex:
    *   we can't allow a trailing decimal after the minimum value,
    *   or a leading decimal before the maximum value
    *   unless there are spaces between the numbers and the ellipsis
    *   because it would be ambiguous with the ellipsis separator.
*   Pattern:
    *   ^\s*            (not captured)
    *   0:  ([\[(])?
        *   Optional left bracket or parenthesis ('[':inclusive|'(':exclusive)
    *   \s*(?:          (not captured)
    *   If no spaces around the ellipsis
        *   1:  ([+-]?\\d*\\.?\\d+(?:[eE][+-]?\\d+)?)
            *   Minimum value (can be float or int)
            *   Cannot end with a decimal (e.g. "1." is not valid)
        *   \.\.        (not captured)
        *   2:  ([+-]?\\d+\\.?\\d*(?:[eE][+-]?\\d+)?)    
            *   Maximum value (can be float or int)
            *   Cannot start with a decimal (e.g. ".2" is not valid)
    *   If spaces around the ellipsis
        *   3:  ([+-]?(?:\\d*\\.?\\d+|\\d+\\.\\d*)(?:[eE][+-]?\\d+)?)
            *   Minimum value (can be float or int)
            *   Any valid number works here (e.g. "1.", ".2", "1e-5", etc.)
        *   \s+\.\.\s+  (not captured)
        *   4:  ([+-]?(?:\\d*\\.?\\d+|\\d+\\.\\d*)(?:[eE][+-]?\\d+)?)
            *   Maximum value (can be float or int)
            *   Any valid number works here (e.g. "1.", ".2", "1e-5", etc.)
    *   )\s*            (not captured)
    *   5:  ([\])])?
        *   Optional right bracket or parenthesis (']':inclusive|')':exclusive)
    *   \s*$            (not captured)
*   e.g.:   "[ 1 .. 2 ]", "(1 .. 2)", "[1..2)", "(1..2]", "1..2", "1e-5..2e+5", etc.
"""


# Matches standard interval strings
# e.g. "[1 .. 2]", "(1 .. 2)", "[1 .. 2)", "(1 .. 2]", "[-1.5 .. 3.5]", "[-1.5 .. 3.5)", "(-1.5 .. 3.5]", "(-1.5 .. 3.5)", [1.5e-5 .. 2e+5], "(1e-5 .. 2e+5)", "[1e-5 .. 2e+5)", "(-1e-5 .. 2e+5]"
std_interval_rgx_str = rf"([\[(])({num_sct_rgx_str})\ \.\.\ ({num_sct_rgx_str})([\])])"
r"""
# String that can be used as a regex that matches standard interval strings (strict formatting)
*   All numbers must be in standard format (e.g. "1", "2.0", "1.0e-10", etc.)
*   The ellipsis must be surrounded by a single space on each side.
*   The brackets/parentheses must be present.
*   Pattern:
    *   0:  ([\[(])
        *   Left bracket or parenthesis ('[':inclusive|'(':exclusive)
    *   1:  ([+-]?(?:\\d*\\.?\\d+|\\d+\\.\\d*)(?:[eE][+-]?\\d+)?)
        *   Minimum value (can be float or int)
    *   \ \.\.\     (not captured)
        *   Ellipsis (must be surrounded by a single space on each side)
        *   ' .. '
    *   2:  ([+-]?(?:\\d*\\.?\\d+|\\d+\\.\\d*)(?:[eE][+-]?\\d+)?)
        *   Maximum value (can be float or int)
    *   3:  ([\])])
        *   Right bracket or parenthesis (']':inclusive|')':exclusive)
*   e.g.:
    *   "[1 .. 2]", "(1 .. 2)", "[1 .. 2)", "(1 .. 2]",
    *   "[-1.5 .. 3.5]", "[-1.5 .. 3.5)", "(-1.5 .. 3.5]", "(-1.5 .. 3.5)",
    *   [1.5e-10 .. 2.0e+10], "(1e-10 .. 2e+10)", "[1e-10)", "[1e-10 .. 2e+10)", "(-1e-10 .. 2e+10]"
"""

std_interval_rgx = compile(f"^{std_interval_rgx_str}$")

def check_interval_str_match(interval: str) -> Match:
    """
    Check if a string is a valid interval and return the regex match object.
    
    Args:
        interval (str): The string to check.
    
    Returns:
        Match: The regex match object (if valid).
    
    Raises:
        ValueError: If the string is not a valid interval.
    """
    match = interval_rgx.fullmatch(interval)
    if match is None:
        raise ValueError(f"Invalid interval format: {interval}")
    
    # Extract the groups correctly
    groups = match.groups()
    
    # The pattern can match with or without brackets, handle both cases
    if groups[0] is not None:  # Has brackets
        # groups[0] = left bracket, groups[1] = min_val, groups[2] = max_val, groups[3] = right bracket
        min_val, max_val = groups[1], groups[2]
    else:  # No brackets
        # groups[4] = min_val, groups[5] = max_val
        min_val, max_val = groups[4], groups[5]
    
    # Check that the minimum value is less than or equal to the maximum value
    if to_number(min_val) > to_number(max_val):
        raise ValueError(f"Minimum value is greater than maximum value: {interval}")
    
    return match

def check_std_interval_str_match(interval: str) -> Match:
    """
    Check if a string is in the standard interval format.
    
    Args:
        interval (str): The string to check.
    
    Returns:
        Match: The regex match object (if valid).
    
    Raises:
        ValueError: If the string is not in the standard interval format.
    """
    match = std_interval_rgx.fullmatch(interval)
    if match is None:
        raise ValueError(f"Invalid standard interval format: {interval}")
    
    # For the standard interval regex, the groups are always in the same order:
    # groups[0] = full match, groups[1] = left bracket, groups[2] = min_val, groups[3] = max_val, groups[4] = right bracket
    groups = match.groups()
    min_val, max_val = groups[1], groups[2]
    
    # Check that the minimum value is less than or equal to the maximum value
    if to_number(min_val) > to_number(max_val):
        raise ValueError(f"Minimum value is greater than maximum value: {interval}")
    
    return match

def check_valid_interval_values(min_val: Union[int, float], max_val: Union[int, float]) -> Tuple[Union[int, float], Union[int, float]]:
    """
    Check that the minimum value is less than or equal to the maximum value.
    
    Args:
        min_val (Union[int, float]): The minimum value.
        max_val (Union[int, float]): The maximum value.
        
    Returns:
        Tuple[Union[int, float], Union[int, float]]: The minimum and maximum values.
    
    Raises:
        ValueError: If the minimum value is greater than the maximum value.
    """
    if min_val > max_val:
        raise ValueError(f"Minimum value is greater than maximum value: {min_val} > {max_val}")
    
    return min_val, max_val

def format_interval(interval: Interval) -> str:
    """
    Convert a sympy Interval to a string.
        
    Args:
        interval (Interval|str): The interval to convert.
        
    Returns:
        str: The string representation of the interval.
    
    Raises:
        ValueError: If the interval is None.
    """
    assert interval is not None, "Interval cannot be None"
    
    # Square brackets [] mean inclusive, parentheses () mean exclusive
    left_bracket = "(" if interval.left_open else "["
    right_bracket = ")" if interval.right_open else "]"
    return f"{left_bracket}{format_number(interval.start)} .. {format_number(interval.end)}{right_bracket}"

def is_float_interval(interval: Interval) -> bool:
    """
    Determine if an interval contains only floats.
    
    Args:
        interval (Interval): The interval to check.
        
    Returns:
        bool: True if the interval contains only floats, False otherwise.
    """
    return not(is_int_interval(interval))

def is_int_interval(interval: Interval) -> bool:
    """
    Determine if an interval contains only integers.
    
    Args:
        interval (Interval): The interval to check.
        
    Returns:
        bool: True if the interval contains only integers, False otherwise.
    """
    # Note: Both the start and end of the interval will be of the same type.
    # This means we don't have to check both start and end.
    # Additionally, we only care about type, not value. So 1.0 is not an int.
    return isinstance(interval.start, int)

def is_interval_str(interval: str) -> bool:
    """
    Determine if a string is a valid interval.
    
    Args:
        interval (str): The string to check.
        
    Returns:
        bool: True if the string is a valid interval, False otherwise.
    """
    match = interval_rgx.fullmatch(interval)
    return match is not None and to_number(match.group(2)) <= to_number(match.group(3))

def is_std_interval_str(interval: str) -> bool:
    """
    Determine if a string is in the standard interval format.
    
    Args:
        interval (str): The string to check.
        
    Returns:
        bool: True if the string is in the standard interval format, False otherwise.
    """
    match = std_interval_rgx.fullmatch(interval)
    return match is not None and to_number(match.group(2)) <= to_number(match.group(3))

def to_interval(interval: str) -> Interval:
    """
    Convert a string to a sympy Interval.
    
    Format explanation:
        The first number is the minimum value, and the second number is the maximum value.
        Intervals can be open or closed on the left and/or right.
        Brackets may be omitted, which assumes a closed interval.
        Syntax:
            [ or ]          - Square brackets indicate a closed (inclusive) interval.
            ( or )          - Parentheses indicate an open (exclusive) interval.
            ".." or "..."   - Two or three period ellipsis
    Format:
        "[a..b]" - Closed interval
        "(a..b)" - Open interval
        "[a..b)" - Left-closed, right-open interval
        "(a..b]" - Left-open, right-closed interval
    
    Args:
        interval (str): The string to convert.
        
    Returns:
        Interval: The sympy Interval.
        
    Raises:
        ValueError: If the string is not a valid interval format
    """
    # Check if matches regex
    match = check_interval_str_match(interval)
    
    # Parse the interval
    left_bracket, min_val, max_val, right_bracket = match.groups()
    # Determine if float or int (look for decimal or scientific notation)
    start       = to_number(min_val)
    end         = to_number(max_val)
    left_open   = left_bracket == "("
    right_open  = right_bracket == ")"
    
    return Interval(start, end, left_open, right_open)

def to_std_interval_str(interval: str) -> str:
    """
    Convert an interval string to the standard format.
    
    Args:
        interval (str): The interval string to convert.
    
    Returns:
        str: The interval string in standard format.
    
    Raises:
        ValueError: If the interval string is not in a valid format.
    """
    # Check if matches regex
    match = check_interval_str_match(interval)
    
    # Check if already in standard format
    if is_std_interval_str(interval):
        return interval
    
    # Extract the components of the interval
    groups = match.groups()
    
    # The pattern can match with or without brackets, handle both cases
    if groups[0] is not None:  # Has brackets
        # groups[0] = left bracket, groups[1] = min_val, groups[2] = max_val, groups[3] = right bracket
        left_bracket = groups[0]
        min_val = groups[1]
        max_val = groups[2]
        right_bracket = groups[3]
    else:  # No brackets
        # groups[4] = min_val, groups[5] = max_val
        left_bracket = "["
        min_val = groups[4]
        max_val = groups[5]
        right_bracket = "]"
    
    # Format the numbers to ensure they're properly represented
    min_val_formatted = format_number(to_number(min_val))
    max_val_formatted = format_number(to_number(max_val))
    
    # Construct the standardized interval string
    std_interval = f"{left_bracket}{min_val_formatted} .. {max_val_formatted}{right_bracket}"
    
    # Sanity check that it's now in standard format
    check_std_interval_str_match(std_interval)
    
    return std_interval

# Override the __str__ method for the Interval class
Interval.__str__ = lambda self: format_interval(self)