"""
Common Utilities

This module provides common utility functions for path management, string formatting, etc.

Copyright 2025 Daniel Robert Jackson
"""

from .intervals import check_interval_str_match, check_std_interval_str_match, check_valid_interval_values, format_interval, interval_rgx, interval_rgx_str, is_float_interval, is_int_interval, is_interval_str, is_std_interval_str, std_interval_rgx, std_interval_rgx_str, to_interval, to_std_interval_str
from .paths     import BaseProjectPaths
from .numbers   import flt_bsc_rgx, flt_bsc_rgx_str, flt_rgx, flt_rgx_str, format_number, int_rgx, int_rgx_str, is_float, is_int, is_number, led_dec_opt_rgx_str, led_dec_req_rgx_str, num_bsc_rgx, num_bsc_rgx_str, num_rgx, num_rgx_str, sci_rgx, sci_rgx_str, sgn_opt_rgx_str, strct_flt_rgx_str, strct_num_rgx, strct_num_rgx_str, to_number, trl_dec_opt_rgx_str, trl_dec_req_rgx_str
from .times     import format_run_time




__all__ = [
    "BaseProjectPaths",
    "check_interval_str_match",
    "check_std_interval_str_match",
    "check_valid_interval_values",
    "flt_bsc_rgx",
    "flt_bsc_rgx_str",
    "flt_rgx",
    "flt_rgx_str",
    "format_interval",
    "format_number",
    "format_run_time",
    "int_rgx",
    "int_rgx_str",
    "interval_rgx",
    "interval_rgx_str",
    "is_float",
    "is_float_interval",
    "is_int",
    "is_int_interval",
    "is_interval",
    "is_interval_str",
    "is_number",
    "is_std_interval_str",
    "led_dec_opt_rgx_str",
    "led_dec_req_rgx_str",
    "num_bsc_rgx",
    "num_bsc_rgx_str",
    "num_rgx",
    "num_rgx_str",
    "sci_rgx",
    "sci_rgx_str",
    "sgn_opt_rgx_str",
    "std_interval_rgx",
    "std_interval_rgx_str",
    "strct_flt_rgx_str",
    "strct_num_rgx",
    "strct_num_rgx_str",
    "to_interval",
    "to_number",
    "to_std_interval_str",
    "trl_dec_opt_rgx_str",
    "trl_dec_req_rgx_str"
]
