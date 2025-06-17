"""
Common String Utilities

This module provides common utility functions for string formatting and parsing

Copyright 2025 Daniel Robert Jackson
"""

from .d_bools import (
    TRUE_RXS,       TRUE_RGX,
    FALSE_RXS,      FALSE_RGX,
    YES_RXS,        YES_RGX,
    NO_RXS,         NO_RGX,
    ON_RXS,         ON_RGX,
    OFF_RXS,        OFF_RGX,
    ENABLED_RXS,    ENABLED_RGX,
    DISABLED_RXS,   DISABLED_RGX,
    TRUE_EXT_RXS,   TRUE_EXT_RGX,
    FALSE_EXT_RXS,  FALSE_EXT_RGX,
    BOOL_RXS,       BOOL_RGX,
    BOOL_EXT_RXS,   BOOL_EXT_RGX,
    check_bool,
    check_true,     check_false,
    check_yes,      check_no,
    check_on,       check_off,
    check_enabled,  check_disabled,
    check_boolish,
    check_trueish,  check_falseish,
    is_bool,
    is_true,        is_false,
    is_yes,         is_no,
    is_on,          is_off,
    is_enabled,     is_disabled,
    is_boolish,
    is_trueish,     is_falseish,
    to_bool,
    interpret_as_bool,
    to_bool_str,
    to_yes_no_str,
    to_on_off_str,
    to_enable_disable_str,
    to_enabled_disabled_str
)
from .d_cases import (
    check_case,       check_case_str,
    is_case,          is_case_str,
    to_case,
    to_case_str,
    CASE_RXS,         CASE_RGX
)
from .d_intervals import (
    check_valid_interval_values,
    extract_interval_elements,
    format_interval,
    is_float_interval,  is_int_interval,    is_interval_str,
    to_interval,
    INTERVAL_RXS,       INTERVAL_RGX
)
from .d_ints import (
    check_int,              check_int_dec,
    check_int_bin,          check_int_hex,      check_int_oct,
    check_int_non_dec,
    check_int_pos,          check_int_neg,
    is_int,                 is_int_dec,
    is_int_bin,             is_int_hex,         is_int_oct,
    is_int_non_dec,
    is_int_pos,             is_int_neg,
    to_int,
    to_int_str,
    to_int_bin_str,         to_int_hex_str,     to_int_oct_str,
    INT_DEC_MAG_RXS,
    INT_DEC_RXS,            INT_DEC_RGX,
    INT_BIN_MAG_DGT_RXS,    INT_BIN_MAG_RXS,
    INT_BIN_RXS,            INT_BIN_RGX,
    INT_HEX_MAG_DGT_RXS,    INT_HEX_MAG_RXS,
    INT_HEX_RXS,            INT_HEX_RGX,
    INT_OCT_MAG_DGT_RXS,    INT_OCT_MAG_RXS,
    INT_OCT_RXS,            INT_OCT_RGX,
    INT_NON_DEC_MAG_RXS,
    INT_NON_DEC_RXS,        INT_NON_DEC_RGX,
    INT_MAG_RXS,
    INT_RXS,                INT_RGX,
)
from .d_numbers import (
    check_float,        check_float_basic,
    check_scinot, check_float_interval,
    is_float,           is_float_basic,
    is_float_scinot,    is_float_interval,
    is_number,          is_scinot,
    to_number,
    to_number_str,
    SCI_RXS,            SCI_RGX,
    FLT_RXS,            FLT_RGX,
    NUM_RXS,            NUM_RGX
)
from .d_reals import (
    check_real,         check_real_digits,
    check_scinot,
    is_real,            is_real_digits,
    is_scinot,
    to_number,
    to_number_str,      to_scinot_str,
    SCI_RXS,            SCI_RGX,
    FLT_RXS,            FLT_RGX,
    NUM_RXS,            NUM_RGX
)
from .d_times import format_run_time

__all__ = [
    "check_valid_interval_values",
    "extract_interval_elements",
    "flt_bsc_rxs",
    "flt_bsc_rgx",
    "flt_rxs",
    "flt_rgx",
    "format_interval",
    "format_number",
    "format_run_time",
    "interval_rxs",
    "interval_rgx",
    "int_bas_rxs",
    "int_bas_rgx",
    "int_bsc_rxs",
    "int_bsc_rgx",
    "int_rxs",
    "int_rgx",
    "is_float_basic",
    "is_basic_int",
    "is_float",
    "is_float_interval",
    "is_int",
    "is_int_interval",
    "is_interval_str",
    "is_non_decimal",
    "is_number",
    "is_scinot",
    "num_rxs",
    "num_rgx",
    "sci_rxs",
    "sci_rgx",
    "to_interval",
    "to_number"
]
