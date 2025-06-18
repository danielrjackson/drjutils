import pytest
from sympy import Interval

from drjutils.common.intervals import (
    check_interval_str_match,
    check_std_interval_str_match,
    check_valid_interval_values,
    format_interval,
    is_float_interval,
    is_int_interval,
    is_interval_str,
    is_std_interval_str,
    to_interval,
    to_std_interval_str,
    interval_rgx,
    std_interval_rgx,
)

VALID_INTERVALS = [
    "[1 .. 2]",
    "(1 .. 2)",
    "[0.5 .. 3.5)",
]

@pytest.mark.parametrize("interval_str", VALID_INTERVALS)
def test_parse_and_format(interval_str):
    match = check_interval_str_match(interval_str)
    assert match is not None
    lb, start, end, rb = match.groups()
    assert check_valid_interval_values(start, end)
    assert is_interval_str(interval_str)

    std = to_std_interval_str(interval_str)
    assert check_std_interval_str_match(std)
    assert std_interval_rgx.fullmatch(std)

    interval = to_interval(interval_str)
    assert check_std_interval_str_match(format_interval(interval))


