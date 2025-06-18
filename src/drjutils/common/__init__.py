"""
Common Utilities

This module provides common utility functions for path management, string formatting, etc.

Copyright 2025 Daniel Robert Jackson
"""

from .numbers import (
    format_number, to_number,
    is_float_basic, is_basic_int, is_float, is_int, is_non_decimal, is_number, is_scinot,
    flt_bsc_rgx, flt_rgx,
    int_bas_rgx, int_bsc_rgx, int_rgx,
    num_rgx,
    sci_rgx,
)
from .intervals import (
    check_valid_interval_values,
    extract_interval_elements,
    format_interval,
    is_float_interval, is_int_interval, is_interval_str,
    to_interval,
    interval_rgx,
)
from .d_paths       import BaseProjectPaths

__all__ = [
    "BaseProjectPaths",
    "check_valid_interval_values",
    "extract_interval_elements",
    "flt_bsc_rgx",
    "flt_rgx",
    "format_interval",
    "format_number",
    "interval_rgx",
    "int_bas_rgx",
    "int_bsc_rgx",
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
    "num_rgx",
    "sci_rgx",
    "to_interval",
    "to_number"
]
