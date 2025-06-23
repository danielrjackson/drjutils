"""Utilities for locating configuration files."""

"""
Standard Libraries
"""
# Path manipulation
from pathlib import Path

"""
Local Libraries
"""
# API keys configuration
from .api_keys import ApiKeys

CONFIG_DIR: Path = Path(__file__).parent
"""Location of the configuration directory."""

API_KEYS_FILE: Path = CONFIG_DIR / "api_keys.yaml"
"""Path to the default ``api_keys.yaml`` configuration file bundled with the package."""

__all__ = [
    "ApiKeys",
    "CONFIG_DIR",
    "API_KEYS_FILE",
]
