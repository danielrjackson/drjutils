"""
Utilities Config Schema Module

This module contains schema definitions for configuration files.

Files:
    api_keys.schema.yaml: Schema for the API keys configuration file

Copyright 2025 Daniel Robert Jackson
"""

"""
Standard Libraries
"""
# Path manipulation
from pathlib import Path

class Path:
    """
    Path for configuration schema folder.

    Attributes:
        root: Path to the configuration schema folder
    """
    def __init__(self):
        self.root = Path(__file__).parent

class Files:
    """
    Paths for configuration schema files.

    Attributes:
        api_keys: Path to the API keys configuration file
    """
    def __init__(self):
        self.api_keys = Path.join(Path.root, "api_keys.schema.yaml")
