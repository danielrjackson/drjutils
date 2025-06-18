"""Simplified interval parsing utilities for tests."""
from __future__ import annotations

import re
from sympy import Interval
from typing import Tuple

interval_rgx = re.compile(r"^\s*([\[(])?\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?|inf(?:inity)?|nan)\s*\.\.\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?|inf(?:inity)?|nan)\s*([\])])?\s*$", re.IGNORECASE)

__all__ = [
    "check_valid_interval_values",
    "extract_interval_elements",
    "format_interval",
    "is_float_interval",
    "is_int_interval",
    "is_interval_str",
    "to_interval",
    "interval_rgx",
]


def extract_interval_elements(interval_str: str) -> Tuple[str, str, str, str]:
    match = interval_rgx.fullmatch(interval_str)
    if not match:
        raise ValueError(f"Invalid interval: {interval_str}")
    lb, start, end, rb = match.groups()
    lb = lb or "["
    rb = rb or "]"
    return lb, start, end, rb


def check_valid_interval_values(start: str, end: str) -> bool:
    return float(start) <= float(end)


def format_interval(interval: str | Interval | dict) -> str:
    if isinstance(interval, Interval):
        lb = "(" if interval.left_open else "["
        rb = ")" if interval.right_open else "]"
        return f"{lb}{interval.start} .. {interval.end}{rb}"
    if isinstance(interval, dict):
        return f"{interval['lb']}{interval['start']} .. {interval['end']}{interval['rb']}"
    lb, start, end, rb = extract_interval_elements(interval)
    return f"{lb}{start} .. {end}{rb}"


def is_float_interval(interval: Interval) -> bool:
    return isinstance(interval.start, float) or isinstance(interval.end, float)


def is_int_interval(interval: Interval) -> bool:
    return isinstance(interval.start, int) and isinstance(interval.end, int)


def is_interval_str(value: str) -> bool:
    try:
        extract_interval_elements(value)
        return True
    except ValueError:
        return False


def to_interval(value: str) -> Interval:
    lb, start, end, rb = extract_interval_elements(value)
    start_v = float(start) if "." in start or "e" in start.lower() else int(start, 0)
    end_v   = float(end) if "." in end or "e" in end.lower() else int(end, 0)
    left_open = lb == "("
    right_open = rb == ")"
    return Interval(start_v, end_v, left_open, right_open)
