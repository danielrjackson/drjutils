"""Basic numeric parsing utilities used in tests."""
from __future__ import annotations

import re
from typing import Union

# Regular expressions for different numeric formats
flt_bsc_rgx = re.compile(r"^\s*[+-]?((\d*\.\d+)|(\d+\.\d*))\s*$")
flt_rgx = re.compile(r"^\s*[+-]?(?:\d*\.\d+|\d+\.\d*|\d+(?:\.\d*)?[eE][+-]?\d+|inf(?:inity)?|nan)\s*$", re.IGNORECASE)
int_bas_rgx = re.compile(r"^\s*[+-]?(?:0x[0-9a-fA-F]+|0b[01]+|0o[0-7]+)\s*$", re.IGNORECASE)
int_bsc_rgx = re.compile(r"^\s*[+-]?\d+\s*$")
int_rgx = re.compile(r"^\s*[+-]?(?:0x[0-9a-fA-F]+|0b[01]+|0o[0-7]+|\d+)\s*$", re.IGNORECASE)
num_rgx = re.compile(r"^(?:" + flt_rgx.pattern[1:-1] + "|" + int_rgx.pattern[1:-1] + ")$", re.IGNORECASE)
sci_rgx = re.compile(r"^\s*[+-]?(?:\d+(?:\.\d*)?|\d*\.\d+)[eE][+-]?\d+\s*$")

__all__ = [
    "format_number",
    "is_float_basic",
    "is_basic_int",
    "is_float",
    "is_int",
    "is_non_decimal",
    "is_number",
    "is_scinot",
    "to_number",
    "flt_bsc_rgx",
    "flt_rgx",
    "int_bas_rgx",
    "int_bsc_rgx",
    "int_rgx",
    "num_rgx",
    "sci_rgx",
]


def format_number(num: Union[int, float]) -> str:
    """Format a number without unnecessary decimals."""
    if isinstance(num, float) and num.is_integer():
        return str(int(num))
    return str(num)


def is_float_basic(value: str) -> bool:
    return flt_bsc_rgx.match(value) is not None


def is_basic_int(value: str) -> bool:
    return int_bsc_rgx.match(value) is not None


def is_float(value: str) -> bool:
    return flt_rgx.match(value) is not None


def is_int(value: str) -> bool:
    return int_rgx.match(value) is not None


def is_non_decimal(value: str) -> bool:
    return re.match(r"^\s*[+-]?(?:0x|0b|0o)", value, re.IGNORECASE) is not None


def is_number(value: str) -> bool:
    return num_rgx.match(value) is not None


def is_scinot(value: str) -> bool:
    return sci_rgx.match(value) is not None


def to_number(value: str) -> Union[int, float]:
    value = value.strip()
    if is_int(value):
        return int(value, 0)
    if is_float(value):
        return float(value)
    raise ValueError(f"Invalid number: {value}")
