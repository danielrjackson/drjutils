"""
Configuration Loader

Handles loading and validation of configuration from YAML files.

Classes:
    ConfigLoader: Load and save configuration from YAML files

Copyright 2025 Daniel Robert Jackson
"""

"""
Standard Libraries
"""
import os
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

"""
Third-Party Libraries
"""
import yaml

# Local imports - use direct import to avoid circular dependency

class ConfigLoader:
    """
    Handles loading and validation of configuration from YAML files.
    
    Attributes:
        config: The loaded configuration
        config_path: The path to the configuration file
    """

    def __init__(self,
                 config_path: str,
                 config_file: str = None,
                 validate_schema: bool = False,
                 schema = None  # Will be typed as ConfigSchema when fully implemented
                 ):
        """
        Initialize the configuration loader.

        Args:
            config_path: The path to the configuration directory or file
            config_file: The name of the configuration file (if config_path is a directory)
            validate_schema: Whether to validate the configuration against a schema
            schema: The schema to validate against (optional)
        """
        # Set up basic logging during initialization
        logging.basicConfig(level=logging.INFO, 
                           format="%(levelname)s: %(message)s")
        
        # Default config path
        if config_path is None:
            raise ValueError("Configuration path must be provided")

        # If the specified path is a file and config_file is not provided
        # then use the specified path as the config file
        # If it's a file and config_file is provided, use the specified path's parent as the directory
        # If it's a directory, use the specified path as the directory
        # In the case of a directory, if config_file is not provided, then assume the file is named 'config.yaml'
        if os.path.isdir(config_path):
            if config_file is None:
                config_file = 'config.yaml'
            self.config_path = Path(os.path.join(config_path, config_file))
        elif os.path.isfile(config_path):
            if config_file is None:
                # extract the file name from the path
                self.config_path = Path(config_path)
            else:
                # Use the specified path's parent and the specified file name
                self.config_path = Path(os.path.join(os.path.dirname(config_path), config_file))
        else:
            raise ValueError(f"Configuration path must be a file or directory: {config_path}")

        self.validate_schema = validate_schema
        self.schema = schema
        self.config = None

        # Load the configuration
        self._load_config()
        
        # Now that we're initialized, we can switch to our enhanced logger if it's available
        try:
            from drjutils.log import info, debug
            info(f"ConfigLoader initialized for {self.config_path}")
        except ImportError:
            logging.info(f"ConfigLoader initialized for {self.config_path}")

    def save_config(self, config: Dict[str, Any] = None, output_path: Optional[str] = None) -> None:
        """
        Save configuration to YAML file.

        Args:
            config: Configuration dictionary to save (defaults to current config)
            output_path: Path to save the configuration to (defaults to loaded path)
        """
        if config is None:
            config = self.config
            
        if output_path is None:
            output_path = self.config_path
        else:
            output_path = Path(output_path)

        # Convert Path objects to strings for serialization
        config_to_save = self._recursively_serialize_config(config)

        # Save configuration
        os.makedirs(output_path.parent, exist_ok=True)
        with open(output_path, 'w') as f:
            yaml.dump(config_to_save, f, default_flow_style=False)
            
        try:
            from drjutils.log import info
            info(f"Configuration saved to {output_path}")
        except ImportError:
            logging.info(f"Configuration saved to {output_path}")

    def _load_config(self):
        """
        Load configuration from YAML file.
        """
        # Check if config file exists
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found at {self.config_path}")

        # Load configuration
        with open(self.config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # Validate configuration against schema if requested
        if self.validate_schema and self.schema is not None:
            self.config = self.schema.validate(self.config)

        try:
            from drjutils.log import debug
            debug(f"Configuration loaded from {self.config_path}")
        except ImportError:
            logging.debug(f"Configuration loaded from {self.config_path}")

    def _recursively_serialize_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recursively serialize configuration to strings.

        Args:
            config: Configuration dictionary to serialize

        Returns:
            Serialized configuration dictionary
        """
        serialized_config = {}
        for key, value in config.items():
            if isinstance(value, dict):
                serialized_config[key] = self._recursively_serialize_config(value)
            elif isinstance(value, Path):
                serialized_config[key] = str(value)
            else:
                serialized_config[key] = value

        return serialized_config
        
    def get(self, key_path, default=None):
        """
        Get a configuration value by key path.
        
        Args:
            key_path (str): Dot-separated path to the configuration value.
            default: Default value to return if key not found.
            
        Returns:
            The configuration value, or default if not found.
        """
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path, value):
        """
        Set a configuration value by key path.
        
        Args:
            key_path (str): Dot-separated path to the configuration value.
            value: Value to set.
        """
        keys = key_path.split('.')
        target = self.config
        
        # Navigate to the target dictionary
        for key in keys[:-1]:
            if key not in target:
                target[key] = {}
            target = target[key]
        
        # Set the value
        target[keys[-1]] = value
        
        try:
            from drjutils.log import debug
            debug(f"Set configuration {key_path} = {value}")
        except ImportError:
            logging.debug(f"Set configuration {key_path} = {value}")
