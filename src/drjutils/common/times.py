"""
Time Formatting Utilities

This module provides utilities for formatting time values.

Functions:
    format_run_time: Format a timedelta as a human-readable string

Copyright 2025 Daniel Robert Jackson
"""

from datetime import timedelta

__all__ = ["format_run_time"]

def format_run_time(td: timedelta) -> str:
    """
    Format a timedelta as a human-readable string.
    
    Formats the timedelta with appropriate units:
    - Days (if present)
    - Hours (if days or hours present)
    - Minutes (if days, hours, or minutes present)
    - Seconds (always shown with millisecond precision)
    
    Args:
        td (timedelta): The timedelta to format
        
    Returns:
        str: A formatted string representation of the timedelta
    
    Examples:
        >>> format_run_time(timedelta(seconds=75))
        '01m 15.000s'
        
        >>> format_run_time(timedelta(days=1, hours=2, minutes=3, seconds=4.5))
        '1d 02h 03m 04.500s'
    """
    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    seconds += td.microseconds / 1e6

    parts = []
    if days:
        parts.append(f"{days}d")
    if hours or days:
        parts.append(f"{hours:02d}h")
    if minutes or hours or days:
        parts.append(f"{minutes:02d}m")
    # Always show seconds with 3 decimal places (milliseconds)
    parts.append(f"{seconds:06.3f}s")
    return " ".join(parts)
