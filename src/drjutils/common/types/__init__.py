"""
# drjutils.common.types

# Types Module

This module provides utility functions for working with various types.

Copyright 2025 Daniel Robert Jackson
"""

from .sentinel import (
    # sentinel
    UNSET,
    # type aliases
    Opt,
    OptOrNone,
    OrNone,
    # methods
    default_factory,
    require,
    resolve,
)
from .type_utils  import (
    T, Many, OneOrMany,
    set_name, set_name_if,
    set_docstring, set_docstring_if,
    set_name_and_doc, set_name_and_doc_if,
    )

__all__ = [
    # sentinel
    "UNSET",
    "Opt",
    "OptOrNone",
    "OrNone",
    "default_factory",
    "require",
    "resolve",
    # type_utils
    "T",
    "Many",
    "OneOrMany",
    "set_name",
    "set_name_if",
    "set_docstring",
    "set_docstring_if",
    "set_name_and_doc",
    "set_name_and_doc_if",
]
