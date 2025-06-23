"""Utilities for locating configuration schema files."""

"""
Standard Libraries
"""
# Path manipulation
from pathlib import Path

SCHEMA_DIR: Path = Path(__file__).parent
"""Directory containing configuration schemas."""

API_KEYS_SCHEMA_FILE: Path = SCHEMA_DIR / "api_keys.schema.yaml"
"""Schema describing the ``api_keys.yaml`` configuration file."""

__all__ = [
    "SCHEMA_DIR",
    "API_KEYS_SCHEMA_FILE",
]
