"""
# __init__.py

## drjutils.common.bools

### Summary

This module provides common utility functions for boolean values and their representations.

### Classes

| Class Name        | Description                                 |
|-------------------|---------------------------------------------|
| `TrueFalse`       | Class for true/false representations.       |
| `YesNo`           | Class for yes/no representations.           |
| `OnOff`           | Class for on/off representations.           |
| `EnabledDisabled` | Class for enabled/disabled representations. |


### Base Classes

| Class Name     | Description                        |
|----------------|------------------------------------|
| `BooleanAlias` | Base class for boolean-like enums. |

Copyright 2025 Daniel Robert Jackson
"""

from .boolean_alias import BooleanAlias
from .true_false import TrueFalse
from .yes_no import YesNo
from .on_off import OnOff
from .enabled_disabled import EnabledDisabled


__all__ = [
    "TrueFalse",
    "YesNo",
    "OnOff",
    "EnabledDisabled",
    "BooleanAlias",
]
