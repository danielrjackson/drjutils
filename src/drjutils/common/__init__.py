"""
Common Utilities

This module provides common utility functions for path management, string formatting, etc.

Copyright 2025 Daniel Robert Jackson
"""

from .intervals import check_interval_str_match, check_valid_interval_values
from .intervals import format_interval, to_interval, to_std_interval_str
from .intervals import is_float_interval, is_int_interval, is_interval_str, is_std_interval_str
from .intervals import interval_rgx_str, interval_rgx
from .paths     import BaseProjectPaths
from .numbers   import format_number, to_number
from .numbers   import is_basic_float, is_basic_int, is_float, is_int, is_non_decimal, is_number, is_scinot
from .numbers   import flt_bsc_rgx_str, flt_bsc_rgx, flt_rgx_str, flt_rgx
from .numbers   import int_bas_rgx_str, int_bas_rgx, int_bsc_rgx_str, int_bsc_rgx, int_rgx_str, int_rgx
from .numbers   import num_opl_rgx_str, num_opl_rgx, num_opt_rgx_str, num_opt_rgx, num_rgx_str, num_rgx
from .numbers   import sci_rgx_str, sci_rgx
from .times     import format_run_time

__all__ = [
    "BaseProjectPaths",
    "check_interval_str_match",
    "check_std_interval_str_match",
    "check_valid_interval_values",
    "flt_bsc_rgx_str",
    "flt_bsc_rgx",
    "flt_rgx_str",
    "flt_rgx",
    "format_interval",
    "format_number",
    "format_run_time",
    "interval_rgx_str",
    "interval_rgx",
    "int_bas_rgx_str",
    "int_bas_rgx",
    "int_bsc_rgx_str",
    "int_bsc_rgx",
    "int_rgx_str",
    "int_rgx",
    "is_basic_float",
    "is_basic_int",
    "is_float",
    "is_float_interval",
    "is_int",
    "is_int_interval",
    "is_interval_str",
    "is_non_decimal",
    "is_number",
    "is_scinot",
    "is_std_interval_str",
    "num_opl_rgx_str",
    "num_opl_rgx",
    "num_opt_rgx_str",
    "num_opt_rgx",
    "num_rgx_str",
    "num_rgx",
    "sci_rgx_str",
    "sci_rgx",
    "std_interval_rgx_str",
    "std_interval_rgx",
    "to_interval",
    "to_number",
    "to_std_interval_str"
]
