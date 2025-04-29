"""
Unit tests for the Numbers module.

Copyright 2025 Daniel Robert Jackson
"""

# Test Libraries
import pytest

# Module Under Test
from drjutils.common.numbers import (
    format_number,
    is_basic_float,
    is_basic_int,
    is_float,
    is_int,
    is_non_decimal,
    is_number,
    is_scinot,
    to_number,
    flt_bsc_rgx,
    flt_rgx,
    int_bas_rgx,
    int_bsc_rgx,
    int_rgx,
    num_opl_rgx,
    num_opt_rgx,
    num_rgx,
    sci_rgx
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
        (" 0.0 ", True),  # Test whitespace handling
        ("42.0", True),
        ("-17.5", True),
        ("3.14", True),
        ("+0.2", True),
        (".7", True),     # No leading zero
        ("1.", True),     # No trailing digit
        ("1e-10", False), # Scientific notation not supported
        ("0", False),     # Integer not supported
        ("42", False),    # Integer not supported
        ("abc", False),   # Non-numeric
        ("", False),      # Empty string
    ])
    def test_is_basic_float(self, num_str, expected):
        """Test basic float validation."""
        assert is_basic_float(num_str) == expected

    @pytest.mark.parametrize("num_str, expected", [
        ("0", True),
        (" 42 ", True),   # Test whitespace handling
        ("42", True),
        ("-17", True),
        ("+123", True),
        ("0012", True),   # Leading zeros
        ("3.14", False),  # Float not supported
        ("1e-10", False), # Scientific notation not supported
        ("0x1a", False),  # Hex not supported in basic
        ("0b101", False), # Binary not supported in basic
        ("abc", False),   # Non-numeric
        ("", False),      # Empty string
    ])
    def test_is_basic_int(self, num_str, expected):
        """Test basic integer validation."""
        assert is_basic_int(num_str) == expected

    @pytest.mark.parametrize("num_str, expected", [
        ("0.0", True),
        (" 42.0 ", True), # Test whitespace handling
        ("42.0", True),
        ("-17.5", True),
        ("3.14", True),
        ("+0.2", True),
        (".7", True),     # No leading zero
        ("1.0e-5", True), # Scientific notation
        ("1.0E+5", True), # Scientific notation with uppercase E
        ("2.3e4", True),  # Scientific notation without sign
        ("56E67", True),  # Scientific notation with integer
        ("inf", True),    # Infinity
        ("INF", True),    # Infinity uppercase
        ("infinity", True), # Full infinity
        ("nAn", True),    # Not a number (case insensitive)
        ("0", False),     # Integer not supported
        ("42", False),    # Integer not supported
        ("0x1a", False),  # Hex not supported
        ("abc", False),   # Non-numeric
        ("", False),      # Empty string
    ])
    def test_is_float(self, num_str, expected):
        """Test float validation."""
        assert is_float(num_str) == expected

    @pytest.mark.parametrize("num_str, expected", [
        ("0", True),
        (" 42 ", True),   # Test whitespace handling
        ("42", True),
        ("-17", True),
        ("+123", True),
        ("0012", True),   # Leading zeros
        ("0x1a", True),   # Hexadecimal
        ("0X1A", True),   # Hexadecimal (uppercase)
        ("0b101", True),  # Binary
        ("0B101", True),  # Binary (uppercase)
        ("0o755", True),  # Octal
        ("0O755", True),  # Octal (uppercase)
        ("-0x1a", True),  # Signed hexadecimal
        ("3.14", False),  # Float not supported
        ("1e-10", False), # Scientific notation not supported
        ("abc", False),   # Non-numeric
        ("", False),      # Empty string
    ])
    def test_is_int(self, num_str, expected):
        """Test integer validation."""
        assert is_int(num_str) == expected

    @pytest.mark.parametrize("num_str, expected", [
        ("0x1a", True),
        (" 0X1A ", True), # Test whitespace handling
        ("0b101", True),
        ("0B101", True),
        ("0o755", True),
        ("0O755", True),
        ("+0x1a", True),  # With positive sign
        ("-0b101", True), # With negative sign
        ("42", False),    # Decimal integer not supported
        ("3.14", False),  # Float not supported
        ("abc", False),   # Non-numeric
        ("", False),      # Empty string
    ])
    def test_is_non_decimal(self, num_str, expected):
        """Test non-decimal number validation."""
        assert is_non_decimal(num_str) == expected

    @pytest.mark.parametrize("num_str, expected", [
        ("0", True),
        (" 42 ", True),   # Test whitespace handling
        ("42", True),
        ("-17", True),
        ("+123", True),
        ("3.14", True),
        ("1e-10", True),
        ("+123.45", True),
        ("-6.78e+2", True),
        (".5", True),     # Leading zero optional
        ("5.", True),     # Trailing zero optional
        ("0x1a", True),   # Hexadecimal
        ("0b101", True),  # Binary
        ("0o755", True),  # Octal
        ("inf", True),    # Infinity
        ("infinity", True), # Full infinity
        ("NaN", True),    # Not a number
        ("abc", False),   # Non-numeric
        ("", False),      # Empty string
    ])
    def test_is_number(self, num_str, expected):
        """Test number validation."""
        assert is_number(num_str) == expected

    @pytest.mark.parametrize("num_str, expected", [
        ("1.0e-5", True),
        (" 1.0E+5 ", True),  # Test whitespace handling
        ("2.3e4", True),
        ("56E67", True),
        (".5e1", True),     # Leading zero optional
        ("5.e1", True),     # Trailing zero optional
        ("0e0", True),      # Zero exponent
        ("+1.2e-3", True),  # With positive sign
        ("-4.5e+6", True),  # With negative sign
        ("1", False),       # Not scientific notation
        ("3.14", False),    # Not scientific notation
        ("abc", False),     # Non-numeric
        ("", False),        # Empty string
    ])
    def test_is_scinot(self, num_str, expected):
        """Test scientific notation validation."""
        assert is_scinot(num_str) == expected

    @pytest.mark.parametrize("num_str, expected", [
        ("0", 0),
        ("42", 42),
        ("-17", -17),
        ("0x1a", 26),     # Hexadecimal
        ("0b101", 5),     # Binary
        ("0o755", 493),   # Octal
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

    def test_regex_basic_float(self):
        """Verify regex patterns for basic float numbers."""
        # Test basic float regex
        assert flt_bsc_rgx.match("3.14") is not None
        assert flt_bsc_rgx.match(" 3.14 ") is not None  # Whitespace
        assert flt_bsc_rgx.match("-17.5") is not None
        assert flt_bsc_rgx.match(".7") is not None      # No leading zero
        assert flt_bsc_rgx.match("7.") is not None      # No trailing digit
        assert flt_bsc_rgx.match("42") is None          # Integer
        assert flt_bsc_rgx.match("1e-5") is None        # Scientific notation

    def test_regex_float(self):
        """Verify regex patterns for float numbers."""
        # Test float regex with all valid formats
        assert flt_rgx.match("3.14") is not None
        assert flt_rgx.match(" 3.14 ") is not None       # Whitespace
        assert flt_rgx.match("1.0e-5") is not None
        assert flt_rgx.match("1.0E+5") is not None       # Uppercase E
        assert flt_rgx.match(".7") is not None           # No leading zero
        assert flt_rgx.match("1.") is not None           # No trailing digit
        assert flt_rgx.match("inf") is not None          # Infinity
        assert flt_rgx.match("INF") is not None          # Uppercase infinity
        assert flt_rgx.match("infinity") is not None     # Full infinity
        assert flt_rgx.match("INFINITY") is not None     # Uppercase full infinity
        assert flt_rgx.match("nan") is not None          # Not a number
        assert flt_rgx.match("NaN") is not None          # Mixed case NaN
        assert flt_rgx.match("42") is None               # Integer

    def test_regex_base_int(self):
        """Verify regex patterns for non-decimal integers."""
        # Test non-decimal base integers
        assert int_bas_rgx.match("0x1a") is not None
        assert int_bas_rgx.match(" 0X1A ") is not None    # Whitespace and uppercase
        assert int_bas_rgx.match("0b101") is not None
        assert int_bas_rgx.match("0B101") is not None     # Uppercase B
        assert int_bas_rgx.match("0o755") is not None
        assert int_bas_rgx.match("0O755") is not None     # Uppercase O
        assert int_bas_rgx.match("+0x1a") is not None     # With sign
        assert int_bas_rgx.match("-0b101") is not None    # With sign
        assert int_bas_rgx.match("42") is None            # Decimal integer
        assert int_bas_rgx.match("0x") is None            # Incomplete hex

    def test_regex_basic_int(self):
        """Verify regex patterns for basic integers."""
        # Test basic integer regex
        assert int_bsc_rgx.match("42") is not None
        assert int_bsc_rgx.match(" 42 ") is not None      # Whitespace
        assert int_bsc_rgx.match("-17") is not None
        assert int_bsc_rgx.match("+123") is not None
        assert int_bsc_rgx.match("0012") is not None      # Leading zeros
        assert int_bsc_rgx.match("3.14") is None          # Float
        assert int_bsc_rgx.match("0x1a") is None          # Hexadecimal

    def test_regex_int(self):
        """Verify regex patterns for all integer types."""
        # Test integer regex with all valid formats
        assert int_rgx.match("42") is not None
        assert int_rgx.match(" 42 ") is not None         # Whitespace
        assert int_rgx.match("-17") is not None
        assert int_rgx.match("+123") is not None
        assert int_rgx.match("0x1a") is not None         # Hexadecimal
        assert int_rgx.match("0X1A") is not None         # Uppercase hex
        assert int_rgx.match("0b101") is not None        # Binary
        assert int_rgx.match("0B101") is not None        # Uppercase binary
        assert int_rgx.match("0o755") is not None        # Octal
        assert int_rgx.match("0O755") is not None        # Uppercase octal
        assert int_rgx.match("3.14") is None             # Float
        assert int_rgx.match("1e-5") is None             # Scientific notation

    def test_regex_number_opl(self):
        """Verify regex patterns for numbers that cannot end with a decimal."""
        # Test number regex for numbers that cannot end with a decimal point
        assert num_opl_rgx.match("42") is not None
        assert num_opl_rgx.match(" 42 ") is not None     # Whitespace
        assert num_opl_rgx.match("3.14") is not None
        assert num_opl_rgx.match(".5") is not None       # Leading zero optional
        assert num_opl_rgx.match("5.") is None           # Ends with decimal
        assert num_opl_rgx.match("1e-5") is not None
        assert num_opl_rgx.match("0x1a") is not None     # Hexadecimal
        assert num_opl_rgx.match("infinity") is not None # Infinity
        assert num_opl_rgx.match("nan") is not None      # Not a number

    def test_regex_number_opt(self):
        """Verify regex patterns for numbers that cannot start with a decimal."""
        # Test number regex for numbers that cannot start with a decimal point
        assert num_opt_rgx.match("42") is not None
        assert num_opt_rgx.match(" 42 ") is not None     # Whitespace
        assert num_opt_rgx.match("3.14") is not None
        assert num_opt_rgx.match(".5") is None           # Starts with decimal
        assert num_opt_rgx.match("5.") is not None       # Trailing zero optional
        assert num_opt_rgx.match("1e-5") is not None
        assert num_opt_rgx.match("0x1a") is not None     # Hexadecimal
        assert num_opt_rgx.match("infinity") is not None # Infinity
        assert num_opt_rgx.match("nan") is not None      # Not a number

    def test_regex_number(self):
        """Verify regex patterns for all number types."""
        # Test number regex with all valid formats
        assert num_rgx.match("42") is not None
        assert num_rgx.match(" 42 ") is not None         # Whitespace
        assert num_rgx.match("3.14") is not None
        assert num_rgx.match("1e-5") is not None
        assert num_rgx.match("+123.45") is not None
        assert num_rgx.match("-6.78e+2") is not None
        assert num_rgx.match(".5") is not None           # Leading zero optional
        assert num_rgx.match("5.") is not None           # Trailing zero optional
        assert num_rgx.match("0x1a") is not None         # Hexadecimal
        assert num_rgx.match("0b101") is not None        # Binary
        assert num_rgx.match("0o755") is not None        # Octal
        assert num_rgx.match("inf") is not None          # Infinity
        assert num_rgx.match("infinity") is not None     # Full infinity
        assert num_rgx.match("nan") is not None          # Not a number
        assert num_rgx.match("abc") is None              # Non-numeric

    def test_regex_scientific(self):
        """Verify regex patterns for scientific notation."""
        # Test scientific notation regex
        assert sci_rgx.match("1.0e-5") is not None
        assert sci_rgx.match(" 1.0E+5 ") is not None     # Whitespace and uppercase E
        assert sci_rgx.match("2.3e4") is not None        # No sign in exponent
        assert sci_rgx.match("5e6") is not None          # Integer mantissa
        assert sci_rgx.match(".5e7") is not None         # No leading zero
        assert sci_rgx.match("8.e9") is not None         # No trailing digit
        assert sci_rgx.match("42") is None               # Not scientific notation
        assert sci_rgx.match("3.14") is None             # Not scientific notation
