"""
Unit tests for the Numbers module.

This module provides comprehensive testing for the number-related utilities 
in the drjutils.common.numbers module.
"""

import pytest
from drjutils.common.numbers import (
    format_number,
    is_float,
    is_int,
    is_number,
    to_number,
    flt_rgx,
    int_rgx,
    num_rgx
)

class TestNumberUtilities:
    """Test suite for number-related utility functions."""

    @pytest.mark.parametrize("input_num, expected", [
        (0, "0"),
        (42, "42"),
        (-17, "-17"),
        (3.14, "3.14"),
        (2.0, "2"),
        (-0.005, "-0.005"),
        (1e-10, "1e-10"),
        (1000000.000001, "1000000.000001"),
    ])
    def test_format_number(self, input_num, expected):
        """Test formatting of numbers to string representation."""
        assert format_number(input_num) == expected

    @pytest.mark.parametrize("num_str, expected", [
        ("0.0", True),
        ("42.0", True),
        ("-17.5", True),
        ("3.14", True),
        ("1e-10", True),
        ("1.23e+5", True),
        ("0", False),
        ("42", False),
        ("abc", False),
        ("", False),
    ])
    def test_is_float(self, num_str, expected):
        """Test float validation."""
        assert is_float(num_str) == expected

    @pytest.mark.parametrize("num_str, expected", [
        ("0", True),
        ("42", True),
        ("-17", True),
        ("+123", True),
        ("3.14", False),
        ("1e-10", False),
        ("abc", False),
        ("", False),
    ])
    def test_is_int(self, num_str, expected):
        """Test integer validation."""
        assert is_int(num_str) == expected

    @pytest.mark.parametrize("num_str, expected", [
        ("0", True),
        ("42", True),
        ("-17", True),
        ("3.14", True),
        ("1e-10", True),
        ("+123.45", True),
        ("-6.78e+2", True),
        ("abc", False),
        ("", False),
    ])
    def test_is_number(self, num_str, expected):
        """Test number validation."""
        assert is_number(num_str) == expected

    @pytest.mark.parametrize("num_str, expected", [
        ("0", 0),
        ("42", 42),
        ("-17", -17),
        ("3.14", 3.14),
        ("1e-10", 1e-10),
        ("+123.45", 123.45),
        ("-6.78e+2", -678.0),
    ])
    def test_to_number(self, num_str, expected):
        """Test conversion of string to number."""
        assert to_number(num_str) == expected

    def test_to_number_invalid(self):
        """Test that invalid number strings raise ValueError."""
        with pytest.raises(ValueError):
            to_number("abc")

    def test_regex_patterns(self):
        """Verify regex patterns for different number types."""
        # Verify float regex
        assert flt_rgx.match("3.14") is not None
        assert flt_rgx.match("1.0e-5") is not None
        assert flt_rgx.match("42") is None

        # Verify integer regex
        assert int_rgx.match("42") is not None
        assert int_rgx.match("-17") is not None
        assert int_rgx.match("3.14") is None

        # Verify generic number regex
        assert num_rgx.match("42") is not None
        assert num_rgx.match("3.14") is not None
        assert num_rgx.match("1e-5") is not None
        assert num_rgx.match("abc") is None
