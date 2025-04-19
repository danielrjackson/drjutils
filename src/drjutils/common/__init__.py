"""
Common Utilities

This module provides common utility functions for path management, string formatting, etc.

Copyright 2025 Daniel Robert Jackson
"""

from .intervals import check_interval_str_match, check_std_interval_str_match, check_valid_interval_values, format_interval, interval_rgx, interval_rgx_str, is_float_interval, is_int_interval, is_interval_str, is_std_interval_str, std_interval_rgx, std_interval_rgx_str, to_interval, to_std_interval_str
from .paths     import BaseProjectPaths
from .numbers   import flt_bsc_opl_rgx_str, flt_bsc_opl_rgx, flt_bsc_opt_rgx_str, flt_bsc_opt_rgx, flt_bsc_rgx_str, flt_bsc_rgx, flt_bsc_rlx_rgx_str, flt_bsc_rlx_rgx, flt_bsc_sct_rgx_str, flt_bsc_sct_rgx, flt_rgx_str, flt_rgx, flt_rlx_rgx_str, flt_rlx_rgx, flt_sct_rgx_str, flt_sct_rgx, format_number, int_rgx_str, int_rgx, int_sct_rgx_str, int_sct_rgx, is_float, is_int, is_number, num_bsc_opl_rgx_str, num_bsc_opl_rgx, num_bsc_opt_rgx_str, num_bsc_opt_rgx, num_bsc_rgx_str, num_bsc_rgx, num_bsc_rlx_rgx_str, num_bsc_rlx_rgx, num_bsc_sct_rgx_str, num_bsc_sct_rgx, num_opl_rgx_str, num_opl_rgx, num_opt_rgx_str, num_opt_rgx, num_rgx_str, num_rgx, num_rlx_rgx_str, num_rlx_rgx, num_sct_rgx_str, num_sct_rgx, sci_rgx_str, sci_rgx, sci_rlx_rgx_str, sci_rlx_rgx, sci_sct_rgx_str, sci_sct_rgx, sgn_opt_rgx_str, sgn_req_rgx_str, to_number
from .times     import format_run_time

__all__ = [
    "BaseProjectPaths",
    "check_interval_str_match",
    "check_std_interval_str_match",
    "check_valid_interval_values",
    "flt_bsc_opl_rgx_str",
    "flt_bsc_opl_rgx",
    "flt_bsc_opt_rgx_str",
    "flt_bsc_opt_rgx",
    "flt_bsc_rgx_str",
    "flt_bsc_rgx",
    "flt_bsc_rlx_rgx_str",
    "flt_bsc_rlx_rgx",
    "flt_bsc_sct_rgx_str",
    "flt_bsc_sct_rgx",
    "flt_rgx_str",
    "flt_rgx",
    "flt_rlx_rgx_str",
    "flt_rlx_rgx",
    "flt_sct_rgx_str",
    "flt_sct_rgx",
    "format_interval",
    "format_number",
    "format_run_time",
    "int_rgx_str",
    "int_rgx",
    "int_sct_rgx_str",
    "int_sct_rgx",
    "is_float",
    "is_float_interval",
    "is_int",
    "is_int_interval",
    "is_interval",
    "is_interval_str",
    "is_number",
    "is_std_interval_str",
    "num_bsc_opl_rgx_str",
    "num_bsc_opl_rgx",
    "num_bsc_opt_rgx_str",
    "num_bsc_opt_rgx",
    "num_bsc_rgx_str",
    "num_bsc_rgx",
    "num_bsc_rlx_rgx_str",
    "num_bsc_rlx_rgx",
    "num_bsc_sct_rgx_str",
    "num_bsc_sct_rgx",
    "num_opl_rgx_str",
    "num_opl_rgx",
    "num_opt_rgx_str",
    "num_opt_rgx",
    "num_rgx_str",
    "num_rgx",
    "num_rlx_rgx_str",
    "num_rlx_rgx",
    "num_sct_rgx_str",
    "num_sct_rgx",
    "sci_rgx_str",
    "sci_rgx",
    "sci_rlx_rgx_str",
    "sci_rlx_rgx",
    "sci_sct_rgx_str",
    "sci_sct_rgx",
    "sgn_opt_rgx_str",
    "sgn_req_rgx_str",
    "to_interval",
    "to_number",
    "to_std_interval_str"
]
