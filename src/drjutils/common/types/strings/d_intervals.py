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
from .d_base_types import (
    format_number, to_number,
    num_rgx_str,
    INF, NEG_INF
    )

__all__ = [
    "check_valid_interval_values",
    "extract_interval_elements",
    "format_interval",
    "interval_rgx_str",
    "interval_rgx",
    "is_float_interval",
    "is_int_interval",
    "is_interval_str",
    "to_interval"
]

_invl_core = rf"(?<start>{num_rgx_str})[\t ]*\.\.[\t ]*(?<end>{num_rgx_str})"
_invl_bkts = r"(?=[\[(][\w\t .+-]+\.\.[\w\t .+-]+[\])]|[\w\t .+-]+\.\.[\w\t .+-]+$)"
_invl_2dts_only = r"(?!.+\.{3,})"
_invl_pfx = rf"{_invl_bkts}(?<lb>[\[(])?[\t ]*{_invl_2dts_only}"
_invl_sfx = r"[\t ]*(?<rb>[\])])?"
interval_rgx_str = rf"{_invl_pfx}{_invl_core}{_invl_sfx}"
r"""
### Numeric Interval Regex String
* Note that in this regex:
    *   we can't allow a trailing decimal after the start value, or a leading decimal before the end
    *   value unless there are spaces between the numbers and the ellipsis because it would be
    *   ambiguous with the ellipsis separator
*   Brackets are optional, and if omitted, the interval is assumed to be closed
    *   `[|]`:inclusive, `(|)`:exclusive
*   The start and end values are separated by an ellipsis (`..`)
    *   The ellipsis can be surrounded by spaces or not
*  The start and end values can be floats or ints in any valid format
    *   e.g. "1.", ".2", "1e-5", "1.0e+5", -inf, inf, etc.
*   e.g.:   "[ 1 .. 2 ]", "(1 .. 2)", "[1..2)", "(1..2]", "1..2", "1e-5..2e+5", etc.
*   Pattern: `(?=[\[(][\w\t .+-]+\.\.[\w\t .+-]+[\])]|[\w\t .+-]+\.\.[\w\t .+-]+$)(?<lb>[\[(])?[\t ]*(?!.+\.{3,})(?<start>[+-]?(?:(?:\d+\.?\d*|\.\d+)(?:e[+-]?\d+)?|0(?:x[\da-f]+|b[01]+|o[0-7]+)|inf(?:inity)?|nan))[\t ]*\.\.[\t ]*(?<end>[+-]?(?:(?:\d+\.?\d*|\.\d+)(?:e[+-]?\d+)?|0(?:x[\da-f]+|b[01]+|o[0-7]+)|inf(?:inity)?|nan))[\t ]*(?<rb>[\])])?`
    *   `(?=...)`                       <br/>Lookahead assertion to check for both or no brackets
        *   With brackets:
            *   `[\[(]`                 <br/>Open bracket or parenthesis
            *   `[\w\t .+-]+`           <br/>Any number-like string
            *   `\.\.`                  <br/>Ellipsis separator
            *   `[\w\t .+-]+`           <br/>Any number-like string
            *   `[\])]`                 <br/>Close bracket or parenthesis
        *   Without brackets:
            *   `[\w\t .+-]+`           <br/>Any number-like string
            *   `\.\.`                  <br/>Ellipsis separator
            *   `[\w\t .+-]+`           <br/>Any number-like string
    0.  `(?<lb>...)?`                   <br/>Optional Capture Group 'lb' (left bracket)
        *   `[\[(]`                     <br/>Open bracket or parenthesis
    *   `[\t ]*`                        <br/>Optional whitespace
    *   `(?!...)`                       <br/>Negative Lookahead assertion
        *  `.+\.{3,}`                   <br/>Ellipsis must be exactly 2 dots
    1.  `(?<start>...)`                 <br/>Capture Group 'start' (lower bound value)
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
    *   `[\t ]*`                        <br/>Optional whitespace
    *   `\.\.`                          <br/>Ellipsis separator
    *   `[\t ]*`                        <br/>Optional whitespace
    2.  `(?<end>...)`                   <br/>Capture Group 'end' (upper bound value)
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
    *   `[\t ]*`                        <br/>Optional whitespace
    3.  `(?<rb>...)?`                   <br/>Optional Capture Group 'rb' (right bracket)
        *   `[\])]`                     <br/>Close bracket or parenthesis
"""

interval_rgx = compile(f"^[\t ]*{interval_rgx_str}[\t ]*$")
r"""
### Numeric Interval Regex
* Note that in this regex:
    *   we can't allow a trailing decimal after the start value, or a leading decimal before the end
    *   value unless there are spaces between the numbers and the ellipsis because it would be
    *   ambiguous with the ellipsis separator
*   Brackets are optional, and if omitted, the interval is assumed to be closed
    *   `[|]`:inclusive, `(|)`:exclusive
*   The start and end values are separated by an ellipsis (`..`)
    *   The ellipsis can be surrounded by spaces or not
*  The start and end values can be floats or ints in any valid format
    *   e.g. "1.", ".2", "1e-5", "1.0e+5", -inf, inf, etc.
*   e.g.:   "[ 1 .. 2 ]", "(1 .. 2)", "[1..2)", "(1..2]", "1..2", "1e-5..2e+5", etc.
*   Pattern: `^[\t ]*(?=[\[(][\w\t .+-]+\.\.[\w\t .+-]+[\])]|[\w\t .+-]+\.\.[\w\t .+-]+$)(?<lb>[\[(])?[\t ]*(?!.+\.{3,})(?<start>[+-]?(?:(?:\d+\.?\d*|\.\d+)(?:e[+-]?\d+)?|0(?:x[\da-f]+|b[01]+|o[0-7]+)|inf(?:inity)?|nan))[\t ]*\.\.[\t ]*(?<end>[+-]?(?:(?:\d+\.?\d*|\.\d+)(?:e[+-]?\d+)?|0(?:x[\da-f]+|b[01]+|o[0-7]+)|inf(?:inity)?|nan))[\t ]*(?<rb>[\])])?[\t ]*$`
    *   `^`                             <br/>Start
    *   `[\t ]*`                        <br/>Optional whitespace
    *   `(?=...)`                       <br/>Lookahead assertion to check for both or no brackets
        *   With brackets:
            *   `[\[(]`                 <br/>Open bracket or parenthesis
            *   `[\w\t .+-]+`           <br/>Any number-like string
            *   `\.\.`                  <br/>Ellipsis separator
            *   `[\w\t .+-]+`           <br/>Any number-like string
            *   `[\])]`                 <br/>Close bracket or parenthesis
        *   Without brackets:
            *   `[\w\t .+-]+`           <br/>Any number-like string
            *   `\.\.`                  <br/>Ellipsis separator
            *   `[\w\t .+-]+`           <br/>Any number-like string
    0.  `(?<lb>...)?`                   <br/>Optional Capture Group 'lb' (left bracket)
        *   `[\[(]`                     <br/>Open bracket or parenthesis
    *   `[\t ]*`                        <br/>Optional whitespace
    *   `(?!...)`                       <br/>Negative Lookahead assertion
        *  `.+\.{3,}`                   <br/>Ellipsis must be exactly 2 dots
    1.  `(?<start>...)`                 <br/>Capture Group 'start' (lower bound value)
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
    *   `[\t ]*`                        <br/>Optional whitespace
    *   `\.\.`                          <br/>Ellipsis separator
    *   `[\t ]*`                        <br/>Optional whitespace
    2.  `(?<end>...)`                   <br/>Capture Group 'end' (upper bound value)
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
    *   `[\t ]*`                        <br/>Optional whitespace
    3.  `(?<rb>...)?`                   <br/>Optional Capture Group 'rb' (right bracket)
        *   `[\])]`                     <br/>Close bracket or parenthesis
    *   `[\t ]*`                        <br/>Optional whitespace
    *   `$`                             <br/>End
"""

__interval_dict_keys = [
    'start', 'end', 'left', 'right', 'left_open', 'right_open'
]



def __is_left_open(left: str) -> bool:
    """
    Convert a string representation of a left bracket to a boolean.
    
    Args:
        left (str): The string to convert.
        * '[':  <br/>Left bracket is closed (i.e. '[')
        * '(':  <br/>Left bracket is open (i.e. '(')
        
    Returns:
        bool: The boolean representation of the left bracket string.
        * True:  <br/>Left bracket is open (i.e. '(')
        * False: <br/>Left bracket is closed (i.e. '[')
    """
    return left == "("

def __is_right_open(right: str) -> bool:
    """
    Convert a string representation of a right bracket to a boolean.
    
    Args:
        right (str): The string to convert.
        * ']':  <br/>Right bracket is closed (i.e. ']')
        * ')':  <br/>Right bracket is open (i.e. ')')
        
    Returns:    
        bool: The boolean representation of the right bracket string.
        * True:  <br/>Right bracket is open (i.e. ')')
        * False: <br/>Right bracket is closed (i.e. ']')
    """
    return right == ")"

def __left_to_str(left: Union[bool, str]) -> str:
    """
    Convert a boolean representation of a left bracket to a string.
    If a string is passed, it is returned as is.
    
    Args:
        left (Union[bool, str]): The boolean to convert.
        * True:  <br/>Left bracket is open (i.e. '(')
        * False: <br/>Left bracket is closed (i.e. '[')
        
    Returns:
        str: The string representation of the left bracket boolean.
    """
    if isinstance(left, str):
        return left
    
    return "(" if left else "["

def __right_to_str(right: Union[bool, str]) -> str:
    """
    Convert a boolean representation of a right bracket to a string.
    If a string is passed, it is returned as is.
    
    Args:
        right (Union[bool, str]): The boolean to convert.
        * True:  <br/>Right bracket is open (i.e. ')')
        * False: <br/>Right bracket is closed (i.e. ']')
        
    Returns:
        str: The string representation of the right bracket boolean.
    """
    if isinstance(right, str):
        return right
    
    return ")" if right else "]"

def __format(
    start:      Union[int, float, str],
    end:        Union[int, float, str],
    left:       Union[str, bool],
    right:      Union[str, bool]) -> str:
    """
    Format an interval as a string.
    
    Args:
        start   (Union[int, float]): The start value of the interval.
        end     (Union[int, float]): The end value of the interval.
        left    (Union[str, bool]): The left bracket of the interval.
        right   (Union[str, bool]): The right bracket of the interval.
    
    Returns:
        str: The formatted interval.
    """
    return f"{__left_to_str(left)}{format_number(start)} .. {format_number(end)}{__right_to_str(right)}"

def _is_interval_dict(interval: dict) -> bool:
    """
    Check if an interval is a dictionary.
    
    Args:
        interval (dict): The interval to check.
        
    Returns:
        bool: True if the interval is a dictionary, False otherwise.
    
    Raises:
        ValueError: If the interval is None.
    """
    assert interval is not None, "Interval cannot be None"
    
    # Check that dictionary has expected keys
    
    return  len(interval) == len(__interval_dict_keys) \
        and all(key in interval             for key in __interval_dict_keys) \
        and all(interval[key] is not None   for key in __interval_dict_keys) \
        and all(isinstance(interval[key], (int, float)) for key in ['start',        'end']) \
        and all(isinstance(interval[key], str)          for key in ['left',         'right']) \
        and all(isinstance(interval[key], bool)         for key in ['left_open',    'right_open']) \
        and interval['left']    in ["[", "("] \
        and interval['right']   in ["]", ")"] \
        and __is_left_open(interval['left'])    == interval['left_open'] \
        and __is_right_open(interval['right'])  == interval['right_open'] \

def _check_is_interval_dict(interval: dict) -> dict:
    """
    Check if an interval is a dictionary.
    
    Args:
        interval (dict): The interval to check.
    
    Returns:
        The passed interval dictionary if valid.
        
    Raises:
        ValueError: If the dictionary is not a valid interval dictionary.
    """
    assert interval is not None, "Interval cannot be None"

    if _is_interval_dict(interval):
        return interval

    if len(interval) != len(__interval_dict_keys):
        raise ValueError(f"Invalid dictionary ({interval}) must have {len(__interval_dict_keys)} keys")

    if any(key not in __interval_dict_keys for key in interval):
        raise ValueError(f"Invalid dictionary ({interval}) must have keys {__interval_dict_keys}")

    if any(interval[key] is None for key in __interval_dict_keys):
        raise ValueError(f"Invalid dictionary ({interval}) must have no None values")
    
    if not all(isinstance(interval[key], (int, float)) for key in ['start', 'end']):
        raise ValueError(f"Invalid dictionary ({interval}) must have 'start' and 'end' as int or float")
    
    if not all(isinstance(interval[key], str) for key in ['left', 'right']):
        raise ValueError(f"Invalid dictionary ({interval}) must have 'left' and 'right' as str")
    
    if not all(isinstance(interval[key], bool) for key in ['left_open', 'right_open']):
        raise ValueError(f"Invalid dictionary ({interval}) must have 'left_open' and 'right_open' as bool")
    
    if interval['left'] not in ["[", "("]:
        raise ValueError(f"Invalid dictionary ({interval}) must have 'left' as '[' or '('")
    
    if interval['right'] not in ["]", ")"]:
        raise ValueError(f"Invalid dictionary ({interval}) must have 'right' as ']' or ')'")
    
    if __is_left_open(interval['left']) != interval['left_open']:
        raise ValueError(f"Invalid dictionary ({interval}) left bracket '{interval['left']}' does not match left_open '{interval['left_open']}'")
    
    if __is_right_open(interval['right']) != interval['right_open']:
        raise ValueError(f"Invalid dictionary ({interval}) right bracket '{interval['right']}' does not match right_open '{interval['right_open']}'")
    
    raise ValueError("A bug has occurred while checking the interval dictionary")

def _match_to_interval_dict(match: Match) -> dict:
    """
    Convert a match object to a dictionary.
    
    Args:
        match (Match): The match object.
    
    Returns:
        dict: The interval dictionary.
            *   left_bracket:   <br/>'[' or '('
            *   right_bracket:  <br/>']' or ')'
            *   start:          <br/>lower bound value
            *   end:            <br/>upper bound value
            *   left_open:      <br/>True if left bracket is '('
            *   right_open:     <br/>True if right bracket is ')'
        or None if the match is None.
    """
    if match is None:
        return None
    
    groups = match.groupdict()

    start   = groups['start']
    end     = groups['end']
    left    = groups['lb']
    right   = groups['rb']

    if (left is None):
        left    = "(" if start  == NEG_INF  else "["
    if (right is None):
        right   = ")" if end    == INF      else "]"
    
    return {
        'start':        start,
        'end':          end,
        'left':         left,
        'right':        right,
        'left_open':    left   == "(",
        'right_open':   right  == ")"
        }

def __match_to_interval_tuple(match: Match) -> Tuple[float, float, str, str, bool, bool]:
    """
    Convert a match object to a dictionary.
    
    Args:
        match (Match): The match object.
    
    Returns: A tuple of the elements of the interval.
            *   left_bracket:   <br/>'[' or '('
            *   right_bracket:  <br/>']' or ')'
            *   start:          <br/>lower bound value
            *   end:            <br/>upper bound value
            *   left_open:      <br/>True if left bracket is '('
            *   right_open:     <br/>True if right bracket is ')'
        or None if the match is None.
    """
    if match is None:
        return None
    
    groups = match.groupdict()

    start   = groups['start']
    end     = groups['end']
    left    = groups['lb']
    right   = groups['rb']

    if (left is None):
        left    = "(" if start  == NEG_INF  else "["
    if (right is None):
        right   = ")" if end    == INF      else "]"
    
    return (
        start,
        end,
        left,
        right,
        left   == "(",
        right  == ")"
        )

def _extract_interval_elements(interval: str) -> Tuple[float, float, str, str, bool, bool]:
    """
    Extract the elements of an interval from a string.
    Does not perform extra validations beyond string format.
    
    Args:
        interval (str): The string to check.
    
    Returns: A tuple of the elements of the interval.
        *   left_bracket:   <br/>'[' or '('
        *   right_bracket:  <br/>']' or ')'
        *   start:          <br/>lower bound value (int or float)
        *   end:            <br/>upper bound value (int or float)
        *   left_open:      <br/>True if left bracket is '('
        *   right_open:     <br/>True if right bracket is ')'
        *   or None if the string could not be parsed as an interval.
    """
    return _match_to_interval_dict(interval_rgx.fullmatch(interval))

def _to_interval_dict(interval: Interval) -> dict:
    """
    Convert an sympy Interval to an internal interval dictionary.
    
    Args:
        interval (Interval): The interval to convert.
        
    Returns:
        dict: The interval dictionary.
    """
    return {
        'start':        interval.start,
        'end':          interval.end,
        'left':         "(" if interval.left_open else "[",
        'right':        ")" if interval.right_open else "]",
        'left_open':    interval.left_open,
        'right_open':   interval.right_open
        }

def _to_interval_tuple(interval: Union[Interval, str, dict]) -> Tuple[float, float, str, str, bool, bool]:
    """
    Convert an interval to a tuple of the values used internally in this module.
    
    Args:
        interval (Union[Interval, str, dict]): The interval to convert.
        
    Returns:
        Tuple[float, float, str, str, bool, bool]: The interval tuple.
        *   start:      <br/>lower bound value
        *   end:        <br/>upper bound value
        *   left:       <br/>'[' or '('
        *   right:      <br/>']' or ')'
        *   left_open:  <br/>True if left bracket is '('
        *   right_open: <br/>True if right bracket is ')'
    """
    if isinstance(interval, str):
        interval = _extract_interval_elements(interval)
    elif isinstance(interval, Interval):
        interval = _to_interval_dict(interval)
    else:
        interval = _check_is_interval_dict(interval)

    return (
        interval['start'],
        interval['end'],
        interval['left'],
        interval['right'],
        interval['left_open'],
        interval['right_open']
    )

def _check_interval_valid(
    start:      Union[int, float],
    end:        Union[int, float],
    left:       str = None,
    right:      str = None,
    left_open:  bool = None,
    right_open: bool = None) -> None:
    """
    Check if an interval is valid.
    
    Args:
        start (Union[int, float]): The start value of the interval.
        end (Union[int, float]): The end value of the interval.
        left (str): The left bracket of the interval.
        right (str): The right bracket of the interval.
        left_open (bool): True if the left bracket is open.
        right_open (bool): True if the right bracket is open.
    
    Raises:
        ValueError: If the interval is not valid.
    """
    if start > end:
        raise ValueError(f"Invalid interval: {start} > {end}")


def check_interval_valid(interval: Union[Interval, str, dict]) -> Union[Interval, str, dict]:
    """
    Check if an interval is valid. Return the passed interval if valid.
    
    Args:
        interval (Union[Interval, str, dict]): The interval to check.
        
    Returns:
        Union[Interval, str, dict]: The passed interval if valid.
    
    Raises:
        ValueError: If the interval is not valid.
    """
    # If the interval is valid, just return it and skip the rest of the function
    # This method checks for interval being None or an invalid dictionary,
    # so we don't need to check for those cases again here.
    if is_interval_valid(interval):
        return interval
    
    if isinstance(interval, str):
        interval = _extract_interval_elements(interval)
        if interval is None:
            raise ValueError(f"Invalid interval string: {interval}")
    elif isinstance(interval, Interval):
        interval = _to_interval_dict(interval)
    elif not _is_interval_dict(interval):
        raise ValueError(f"Invalid interval dictionary: {interval}")
    
    if isinstance(interval, dict):
        start       = interval['start']
        end         = interval['end']
        left_open   = interval['left_open']
        right_open  = interval['right_open']
    else:
        start       = interval.start
        end         = interval.end
        left_open   = interval.left_open
        right_open  = interval.right_open
    
    if start > end:
        raise ValueError(f"Invalid interval: {start} > {end}")
    if start == NEG_INF and not left_open:
        raise ValueError(f"Invalid interval: {start} is not open")
    if end   == INF     and not right_open:
        raise ValueError(f"Invalid interval: {end} is not open")
    

def is_interval_valid(interval: Union[Interval, str, dict]) -> bool:
    """
    Check if an interval is valid.
    
    Args:
        interval_elements (Union[Interval, str, dict]): The interval to check.
        
    Returns:
        bool: True if the interval is valid, False otherwise.
        
    Raises:
        ValueError:
        *   If an interval dictionary is passed and it does not have the expected keys.
        *   If the interval is None.
    """
    if interval is None:
        raise ValueError("Interval cannot be None")
    
    if isinstance(interval, dict) and not _is_interval_dict(interval):
        raise ValueError(f"Invalid interval dictionary: {interval}")
    
    if isinstance(interval, str):
        interval = _extract_interval_elements(interval)
        if interval is None:
            return False

    if isinstance(interval, dict):
        left_open   = interval['lb'] == "("
        right_open  = interval['rb'] == ")"
        start       = interval['start']
        end         = interval['end']
    elif isinstance(interval, Interval):
        left_open   = interval.left_open
        right_open  = interval.right_open
        start       = interval.start
        end         = interval.end

    ordered             = start <= end
    is_start_neg_inf    = start == NEG_INF
    is_end_pos_inf      = end   == INF
    lb_valid            = is_start_neg_inf  and left_open   or not is_start_neg_inf
    rb_valid            = is_end_pos_inf    and right_open  or not is_end_pos_inf
    return ordered and lb_valid and rb_valid

def extract_interval_elements(interval: str) -> dict:
    """
    Check if a string is a valid interval and return the elements of the interval.
    
    Args:
        interval (str): The string to check.
    
    Returns:
        dict: The elements of the interval.
            *   lb:     left bracket
            *   rb:     right bracket
            *   start:  lower bound value
            *   end:    upper bound value

    Raises:
        ValueError: If the string is not a valid interval.
    """
    match = interval_rgx.fullmatch(interval)

    if match is None:
        raise ValueError(f"Invalid interval format: {interval}")

    # Extract the groups correctly
    groups = match.groupdict()

    start           = groups['start']
    end             = groups['end']
    left_bracket    = groups['lb']
    right_bracket   = groups['rb']

    if (left_bracket is None):
        left_bracket = "("  if start    == NEG_INF else "["
    if (right_bracket is None):
        right_bracket = ")" if end      == INF else "]"

    interval_dict = {
        'start':    start,
        'end':      end,
        'lb':       left_bracket,
        'rb':       right_bracket
    }

    # Check if the minimum value is less than or equal to the maximum value
    check_valid_interval_values(interval_dict['start'], interval_dict['end'])

    return interval_dict

def format_interval(interval: Union[Interval, str, dict]) -> str:
    """
    Convert an sympy Interval or interval string to the standard string format.
        
    Args:
        interval (Interval|str|dict): The interval to convert.
        
    Returns:
        str: The string representation of the interval.
    
    Raises:
        ValueError: If the interval is None.
    """
    assert interval is not None, "Interval cannot be None"
    
    if isinstance(interval, str):
        interval = _extract_interval_elements(interval)
    
    if isinstance(interval, dict):
        start   = interval['start']
        end     = interval['end']
        left    = interval['left']
        right   = interval['right']
    elif isinstance(interval, Interval):
        # If the interval is a sympy Interval, extract the elements
        start   = interval.start
        end     = interval.end
        left    = "[" if interval.left_open else "("
        right   = "]" if interval.right_open else ")"
    else:
        # This would represent a bug in the code, as we should only be able to pass a string or a sympy Interval
        raise ValueError(f"Invalid interval type: {type(interval)}. Must be a string or sympy Interval.")
    
    return f"{left_bracket}{start} .. {end}{right_bracket}"

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
    
    * The string should match the format of a numeric intervals.
    * The start value must be less than or equal to the end value.
    * The left bracket must be "[" or "(" and the right bracket must be "]" or ")".
    
    
    Args:
        interval (str): The string to check.
        
    Returns:
        bool: True if the string is a valid interval, False otherwise.
    """
    match = interval_rgx.fullmatch(interval)
    
    if match is None:
        return False
    
    groups = match.groupdict()
    
    # Verify that the start value is less than or equal to the end value
    left_bracket    = groups['lb']
    right_bracket   = groups['rb']
    start           = to_number(groups['start'])
    end             = to_number(groups['end'])
    
    # Check that the interval is valid.
    return is_interval_valid({
        'lb': left_bracket,
        'rb': right_bracket,
        'start': start,
        'end': end
    })
    
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
    # Check if the string is a valid interval
    interval_elements = extract_interval_elements(interval)
    
    start       = interval_elements['start']
    end         = interval_elements['end']
    left_open   = interval_elements['lb'] == "("
    right_open  = interval_elements['rb'] == ")"
    
    return Interval(start, end, left_open, right_open)

# Override the __str__ method for the Interval class
Interval.__str__ = lambda self: format_interval(self)