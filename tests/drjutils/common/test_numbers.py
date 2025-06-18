import pytest

from drjutils.common.numbers import (
    format_number,
    is_float_basic,
    is_basic_int,
    is_float,
    is_int,
    is_number,
    is_scinot,
    to_number,
    flt_bsc_rgx,
    flt_rgx,
    int_bas_rgx,
    int_bsc_rgx,
    int_rgx,
    num_rgx,
    sci_rgx,
)

class TestNumberUtilities:
    @pytest.mark.parametrize("input_num, expected", [
        (0, "0"),
        (42, "42"),
        (-17, "-17"),
        (3.14, "3.14"),
    ])
    def test_format_number(self, input_num, expected):
        assert format_number(input_num) == expected

    @pytest.mark.parametrize("num_str, expected", [
        ("0.0", True),
        ("42.0", True),
        ("-17.5", True),
        ("3.14", True),
        ("0", False),
        ("abc", False),
    ])
    def test_is_float_basic(self, num_str, expected):
        assert is_float_basic(num_str) == expected

    @pytest.mark.parametrize("num_str, expected", [
        ("0", True),
        ("42", True),
        ("-17", True),
        ("+123", True),
        ("3.14", False),
        ("abc", False),
    ])
    def test_is_basic_int(self, num_str, expected):
        assert is_basic_int(num_str) == expected

    @pytest.mark.parametrize("num_str, expected", [
        ("0.0", True),
        ("1.0e-5", True),
        ("42", False),
    ])
    def test_is_float(self, num_str, expected):
        assert is_float(num_str) == expected

    @pytest.mark.parametrize("num_str, expected", [
        ("0", True),
        ("42", True),
        ("-17", True),
        ("3.14", False),
    ])
    def test_is_int(self, num_str, expected):
        assert is_int(num_str) == expected

    @pytest.mark.parametrize("num_str, expected", [
        ("0", True),
        ("3.14", True),
        ("1e-5", True),
        ("abc", False),
    ])
    def test_is_number(self, num_str, expected):
        assert is_number(num_str) == expected

    @pytest.mark.parametrize("num_str, expected", [
        ("1e-5", True),
        ("+1.2e-3", True),
        ("1", False),
    ])
    def test_is_scinot(self, num_str, expected):
        assert is_scinot(num_str) == expected

    @pytest.mark.parametrize("num_str, expected", [
        ("0", 0),
        ("42", 42),
        ("3.14", 3.14),
    ])
    def test_to_number(self, num_str, expected):
        assert to_number(num_str) == expected

    def test_to_number_invalid(self):
        with pytest.raises(ValueError):
            to_number("abc")

    def test_regexes(self):
        assert flt_bsc_rgx.match("3.14")
        assert flt_rgx.match("1e-5")
        assert int_bas_rgx.match("42")
        assert int_bsc_rgx.match("42")
        assert int_rgx.match("42")
        assert num_rgx.match("42")
        assert sci_rgx.match("1e-5")
