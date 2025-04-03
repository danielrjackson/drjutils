"""
Utilities Config Module

This module contains general configuration useful in most projects.

Classes:
    ApiKeys: Represents an API key configuration

Copyright 2025 Daniel Robert Jackson
"""

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

__all__ = ['ApiKeys']

class Path:
    """
    Path for configuration folder.

    Attributes:
        root: Path to the configuration folder
    """
    def __init__(self):
        self.root = Path(__file__).parent

class Files:
    """
    Paths for configuration files.

    Attributes:
        api_keys: Path to the API keys configuration file
    """
    def __init__(self):
        self.api_keys = Path.join(Path.root, "api_keys.yaml")
