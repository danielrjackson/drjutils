"""
Common Utilities

This module provides common utility functions for path management, string formatting, etc.

Copyright 2025 Daniel Robert Jackson
"""

from .d_base_types  import (
    format_number, to_number,
    is_float_basic, is_basic_int, is_float, is_int, is_not_base10_int, is_number, is_scinot,
    flt_bsc_rxs, flt_bsc_rgx, flt_rxs, flt_rgx,
    int_bas_rxs, int_bas_rgx, int_bsc_rxs, int_bsc_rgx, int_rxs, int_rgx,
    num_rxs, num_rgx,
    sci_rxs, sci_rgx)
from .d_intervals   import (
    check_valid_interval_values,
    extract_interval_elements,
    format_interval,
    is_float_interval, is_int_interval, is_interval_str,
    to_interval,
    interval_rxs, interval_rgx
    )
from .d_paths       import BaseProjectPaths
from .d_times       import format_run_time

__all__ = [
    "BaseProjectPaths",
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
