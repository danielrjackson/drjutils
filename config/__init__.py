"""
Daniel's Utilities Project Configuration

This file contains paths for the Training-Models project configuration files.

Classes:
    ProjectConfigPath: Folder paths for the project config
        - project_config: Path to the project configuration directory
    ProjectPaths: Folder paths for the project
        - project_root: Path to the project root directory
        - source_root: Path to the project source directory
        - project_config_root: Path to the project configuration directory
        - data: Path to the project data directory where training data is cached
        - logs: Path to the project logs directory where the training logs are saved
        - models: Path to the project models directory where the trained TrainingModels models are saved
    ProjectConfigFiles: File paths for the project config
        - project_config: Path to the project configuration file
        - project_keys: Path to the project keys configuration file

Copyright 2025 Daniel Robert Jackson
"""

import os

class ConfigPath:
    """
    Folder paths for the project config.

    Attributes:
        project_config: Path to the project configuration directory
    """

    def __init__(self):
        """
        Initialize the project paths.
        """
        # Path to the project configuration directory
        self.project_config = os.path.dirname(__file__)

class Paths(ConfigPath):
    """
    Folder paths for the project.

    Contains the Paths inherited from:
        ProjectConfigPath: Contains path for the project config

    Attributes:
        project_root: Path to the project root directory
        source_root: Path to the project source directory
        project_config_root: Path to the project configuration directory
        data: Path to the project data directory where training data is cached
        logs: Path to the project logs directory where the training logs are saved
        models: Path to the project models directory where the trained TrainingModels models are saved
    """

    def __init__(self):
        """
        Initialize the project paths.
        """
        super().__init__()
        # Path to the project root directory
        self.project_root   = os.path.abspath(  os.path.join(os.path.dirname(__file__), ".."))
        # Path to the project source
        self.source_root    =                   os.path.join(self.project_root,         "src")
        # Path to the project logs directory where the training logs are saved
        self.logs           =                   os.path.join(self.project_root,         "logs")


class ConfigFiles:
    """
    File paths for the project config.

    Attributes:
        project_config: Path to the project configuration file
        project_keys: Path to the project keys configuration file
    """

    def __init__(self):
        """
        Initialize the project files.
        """
        # Path to the general project configuration file
        self.project_config = os.path.join(Paths.project_config, "config.yaml")
        
        # Path to the project keys configuration file with information about how to access credentials
        self.project_keys   = os.path.join(Paths.project_config, "keys.yaml")
