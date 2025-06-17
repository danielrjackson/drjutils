"""
Unit tests for the intervals module.
    
Copyright 2025 Daniel Robert Jackson
"""

# Test Libraries
import pytest

# External Libraries
from sympy import Interval

# Module Under Test
from drjutils.common.intervals import (
    check_valid_interval_values,
    extract_interval_elements,
    format_interval,
    is_float_interval, is_int_interval, is_interval_str,
    to_interval,
    interval_rgx
    )

# Test Constants
std_int_intervals = [
    ("[1 .. 2]",            Interval( 1, 2, left_open=False,    right_open=False)),
    ("(1 .. 2)",            Interval( 1, 2, left_open=True,     right_open=True)),
    ("[1 .. 2)",            Interval( 1, 2, left_open=False,    right_open=True)),
    ("(1 .. 2]",            Interval( 1, 2, left_open=True,     right_open=False)),
    ("[-1 .. 0]",           Interval(-1, 0, left_open=False,    right_open=False)),
    ("(-1 .. 0)",           Interval(-1, 0, left_open=True,     right_open=True)),
    ("[0 .. 1)",            Interval( 0, 1, left_open=False,    right_open=True)),
    ("(0 .. 1]",            Interval( 0, 1, left_open=True,     right_open=False)),
    ("[-1 .. 1]",           Interval(-1, 1, left_open=False,    right_open=False))
]

valid_int_intervals = std_int_intervals + [
    ("[1..2]",              Interval(1, 2, left_open=False, right_open=False)),
    ("(1..2)",              Interval(1, 2, left_open=True,  right_open=True)),
    ("[1..2)",              Interval(1, 2, left_open=False, right_open=True)),
    ("(1..2]",              Interval(1, 2, left_open=True,  right_open=False)),
    ("[1 .. 2] ",           Interval(1, 2, left_open=False, right_open=False)),
    (" (1 .. 2)",           Interval(1, 2, left_open=True,  right_open=True)),
    ("[1 .. 2 ]",           Interval(1, 2, left_open=False, right_open=False)),
    ("[ 1 ..2 )",           Interval(1, 2, left_open=False, right_open=True)),
    ("( 1.. 2 ]",           Interval(1, 2, left_open=True,  right_open=False)),
    ("(   1  ..  2  )",     Interval(1, 2, left_open=True,  right_open=True)),
    ("1..2",                Interval(1, 2, left_open=False, right_open=False)),
    ("1 .. 2",              Interval(1, 2, left_open=False, right_open=False)),
    (" 1..2",               Interval(1, 2, left_open=False, right_open=False)),
    ("1..2 ",               Interval(1, 2, left_open=False, right_open=False)),
    ("  1   ..  2    ",     Interval(1, 2, left_open=False, right_open=False)),
    ("[0x0001 .. 0x0002]",  Interval(1, 2, left_open=False, right_open=False))
]

std_float_intervals = [
    ("[0.5 .. 3.5]",        Interval(0.5,           3.5,            left_open=False,    right_open=False)),
    ("(0.5 .. 3.5)",        Interval(0.5,           3.5,            left_open=True,     right_open=True)),
    ("[0.5 .. 3.5)",        Interval(0.5,           3.5,            left_open=False,    right_open=True)),
    ("(0.5 .. 3.5]",        Interval(0.5,           3.5,            left_open=True,     right_open=False)),
    ("[1.0e-5 .. 2.0e+15]", Interval(1.0e-5,        2.0e+15,        left_open=False,    right_open=False)),
    ("(1.0e-5 .. 2.0e+15)", Interval(1.0e-5,        2.0e+15,        left_open=True,     right_open=True)),
    ("[1.0e-5 .. 2.0e+15)", Interval(1.0e-5,        2.0e+15,        left_open=False,    right_open=True)),
    ("(1.0e-5 .. 2.0e+15]", Interval(1.0e-5,        2.0e+15,        left_open=True,     right_open=False)),
    ("[-inf .. inf]",       Interval(float("-inf"), float("inf"),   left_open=False,    right_open=False)),
    ("(-inf .. inf)",       Interval(float("-inf"), float("inf"),   left_open=True,     right_open=True)),
]

valid_float_intervals = std_float_intervals + [
    "[-1.5..3.5]",
    "[-1.5..3.5)",
    "(-1.5..3.5]",
    "(-1.5..3.5)",
    "[-1.5 .. 3.5 ]",
    "[ -1.5.. 3.5 )",
    "( -1.5 ..3.5 ]",
    "( -1.5 .. 3.5)",
    "[ 1e-5 .. 2e+5 ]",
    "( 1e-5 .. 2e+5 )",
    "[ 1e-5 .. 2e+5 )",
    "( 1e-5 .. 2e+5 ]",
    " [-1.5 .. 3.5]",
    "[-1.5 .. 3.5) ",
    "1e-5..2e+5",
    "1e-5 .. 2e+5",
    "1e-5  ..  2e+5",
    " 1e-5..2e+5",
    "1e-5..2e+5 ",
    "   1e-5  .. 2e+5  "
]

std_intervals = std_int_intervals + std_float_intervals
valid_intervals = valid_int_intervals + valid_float_intervals

invalid_intervals = [
    "[2 .. 1]",
    "(2 .. 1)",
    "[2 .. 1)",
    "(2 .. 1]",
    "[1.0 .. -1.0]",
    "1",
    "1.5",
    "-1.5",
    "1..",
    "1...",
    ".2",
    "..2",
    "...2",
    "1 . 2",
    "[1 . 2]",
    "(1 . 2)",
    "1..2..3",
    "1...2...3",
    "[1..2",
    "(1..2",
    "1..2]",
    "1..2)",
    "[1...2",
    "(1...2",
    "1...2]",
    "1...2)",    
    "[1...2]",
    "[ 1...2 )",
    " (1...2] ",
    "1...2",
    "[-1.5 ...3.5]",
    "1e-5...2e+5",
    " 1e-5 ... 2e+5 ",
    "fred",
    ""
]


# Test Cases

# *check_interval_str_match
# *check_std_interval_str_match
# *format_interval
# *is_float_interval
# *is_int_interval
# *interval_rgx
# *is_interval_str
# *is_std_interval_str
# *to_interval
# *to_std_interval_str

@pytest.mark.parametrize("interval_str", valid_intervals)
def test_check_interval_str_match_valid(interval_str):
    assert check_valid_interval_values(interval_str) is not None

@pytest.mark.parametrize("interval_str", invalid_intervals)
def test_check_interval_str_match_invalid(interval_str):
    with pytest.raises(ValueError):
        check_interval_str_match(interval_str)

@pytest.mark.parametrize("interval_str", std_intervals)
def test_check_std_interval_str_match_valid(interval_str):
    assert check_std_interval_str_match(interval_str) is not None

@pytest.mark.parametrize("interval_str", invalid_intervals)
def test_check_std_interval_str_match_invalid(interval_str):
    with pytest.raises(ValueError):
        check_std_interval_str_match(interval_str)

@pytest.mark.parametrize("interval_str", valid_intervals)
def test_check_valid_interval_values_valid(interval_str):
    match = check_interval_str_match(interval_str)
    min_val, max_val = match.groups()[1:3]
    assert check_valid_interval_values(min_val, max_val)    

@pytest.mark.parametrize("interval_str", valid_intervals)
def test_format_interval_and_to_std_interval_str_valid(interval_str):
    assert format_interval(interval_str) == to_std_interval_str(interval_str)

@pytest.mark.parametrize("interval_str", invalid_intervals)
def test_format_interval_invalid(interval_str):
    with pytest.raises(ValueError):
        format_interval(interval_str)

@pytest.mark.parametrize("interval_str", valid_intervals)
def test_interval_rgx(interval_str):
    assert interval_rgx.fullmatch(interval_str)

@pytest.mark.parametrize("interval_str", invalid_intervals)
def test_interval_rgx_invalid(interval_str):
    assert not interval_rgx.fullmatch(interval_str)

@pytest.mark.parametrize("interval_str", valid_float_intervals)
def test_is_float_interval(interval_str):
    interval = to_interval(interval_str)
    assert not is_float_interval(interval)

@pytest.mark.parametrize("interval_str", invalid_intervals)
def test_is_float_interval_invalid(interval_str):
    with pytest.raises(ValueError):
        is_float_interval(to_interval(interval_str))

@pytest.mark.parametrize("interval_str", valid_int_intervals)
def test_is_int_interval(interval_str):
    interval = to_interval(interval_str)
    assert is_int_interval(interval)

@pytest.mark.parametrize("interval_str", invalid_intervals)
def test_is_int_interval_invalid(interval_str):
    with pytest.raises(ValueError):
        is_int_interval(to_interval(interval_str))

@pytest.mark.parametrize("interval_str", valid_intervals)
def test_is_interval_str(interval_str):
    assert is_interval_str(interval_str)

@pytest.mark.parametrize("interval_str", invalid_intervals)
def test_is_interval_invalid(interval_str):
    assert not is_interval_str(interval_str)

@pytest.mark.parametrize("interval_str", valid_intervals)
def test_is_std_interval_str(interval_str):
    assert is_std_interval_str(to_std_interval_str(interval_str))

@pytest.mark.parametrize("interval_str", invalid_intervals)
def test_is_std_interval_str_invalid(interval_str):
    assert not is_std_interval_str(interval_str)
        
@pytest.mark.parametrize("interval_str", valid_intervals)
def test_to_interval_valid(interval_str):
    interval = to_interval(interval_str)
    assert isinstance(interval, Interval)

@pytest.mark.parametrize("interval_str", invalid_intervals)
def test_to_interval_invalid(interval_str):
    with pytest.raises(ValueError):
        to_interval(interval_str)

@pytest.mark.parametrize("interval_str", valid_intervals)
def test_to_std_interval_str_valid(interval_str):
    assert std_interval_rgx.fullmatch(to_std_interval_str(interval_str)) is not None

@pytest.mark.parametrize("interval_str", invalid_intervals)
def test_to_std_interval_str_invalid(interval_str):
    with pytest.raises(ValueError):
        to_std_interval_str(interval_str)
