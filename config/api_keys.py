"""
API Key Management

Utilities for managing API keys stored in credential managers like Windows Credential Manager.
This module helps with retrieving API keys based on a standard configuration format.

Classes:
    ApiKey: Represents an API key configuration
    KeyManager: Manages API keys based on a configuration file

Copyright 2025 Daniel Robert Jackson
"""

import os
from pathlib import Path
from typing import Dict, List, Optional

# Try to import keyring for credential storage
try:
    import keyring
    KEYRING_AVAILABLE = True
except ImportError:
    KEYRING_AVAILABLE = False

# Import our own modules - using relative imports to avoid circular dependencies
from ..log import debug, info, warning, error
from .loader import ConfigLoader

class ApiKey:
    """
    Represents an API key stored in a credential manager.
    
    Attributes:
        name: The name of the key in the config file
        url: The service name in the credential manager
        username: The username for the credential
    """
    
    def __init__(self, name: str, config: Dict):
        """
        Initialize an API key from a configuration dictionary.
        
        Args:
            name: The name of the key in the config file
            config: The configuration dictionary for this key
        """
        self.name = name
        self.url = config.get('url')
        self.username = config.get('username')
        
        if not self.url:
            raise ValueError(f"API key '{name}' is missing the 'url' field")
        if not self.username:
            raise ValueError(f"API key '{name}' is missing the 'username' field")
    
    def get_value(self) -> Optional[str]:
        """
        Retrieve the API key value from the credential manager.
        
        Returns:
            The API key value, or None if it couldn't be retrieved
        """
        if not KEYRING_AVAILABLE:
            warning(f"Keyring not available, can't retrieve key for {self.name}")
            return None
        
        try:
            key = keyring.get_password(self.url, self.username)
            if key is None:
                warning(f"No key found for {self.name} ({self.url}, {self.username})")
            return key
        except Exception as e:
            error(f"Error retrieving key for {self.name}: {e}")
            return None
    
    def set_value(self, value: str) -> bool:
        """
        Set the API key value in the credential manager.
        
        Args:
            value: The API key value to store
            
        Returns:
            True if the key was set successfully, False otherwise
        """
        if not KEYRING_AVAILABLE:
            warning(f"Keyring not available, can't store key for {self.name}")
            return False
        
        try:
            keyring.set_password(self.url, self.username, value)
            info(f"Key for {self.name} stored successfully")
            return True
        except Exception as e:
            error(f"Error storing key for {self.name}: {e}")
            return False
    
    def __str__(self) -> str:
        """Return a string representation of this API key."""
        return f"{self.name} (service: {self.url}, username: {self.username})"


class KeyManager:
    """
    Manages API keys based on a configuration file.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the key manager.
        
        Args:
            config_path: Path to the keys configuration file. If None,
                         attempts to find a keys.yaml file in standard locations.
        """
        self.keys: Dict[str, ApiKey] = {}
        
        # Find keys config if not provided
        if config_path is None:
            from .utils import find_config_file
            config_path = find_config_file("keys.yaml")
            
            if config_path is None:
                warning("No keys.yaml found in standard locations")
                return
        
        try:
            # Load the configuration file
            self.config_loader = ConfigLoader(config_path)
            self._load_keys()
        except Exception as e:
            error(f"Failed to initialize key manager: {e}")
    
    def _load_keys(self):
        """
        Load API keys from the configuration.
        """
        config = self.config_loader.config
        if not config:
            return
        
        # Process each top-level key in the config
        for key_name, key_config in config.items():
            try:
                # Skip any non-dictionary values
                if not isinstance(key_config, dict):
                    continue
                
                api_key = ApiKey(key_name, key_config)
                self.keys[key_name] = api_key
                debug(f"Loaded API key configuration: {api_key}")
            except ValueError as e:
                warning(str(e))
    
    def get_key(self, name: str) -> Optional[str]:
        """
        Get an API key value by name.
        
        Args:
            name: The name of the API key
            
        Returns:
            The API key value, or None if not found
        """
        if name not in self.keys:
            warning(f"API key '{name}' not found in configuration")
            return None
        
        return self.keys[name].get_value()
    
    def get_all_keys(self) -> List[ApiKey]:
        """
        Get all configured API keys.
        
        Returns:
            A list of all API keys
        """
        return list(self.keys.values())
    
    def get_key_config(self, name: str) -> Optional[ApiKey]:
        """
        Get an API key configuration by name.
        
        Args:
            name: The name of the API key
            
        Returns:
            The API key configuration, or None if not found
        """
        return self.keys.get(name)


# Convenience function to get a singleton instance
_key_manager_instance = None

def get_key_manager(config_path: Optional[str] = None) -> KeyManager:
    """
    Get a KeyManager instance.
    
    Args:
        config_path: Path to the keys configuration file
        
    Returns:
        A KeyManager instance
    """
    global _key_manager_instance
    if _key_manager_instance is None:
        _key_manager_instance = KeyManager(config_path)
    return _key_manager_instance


def get_api_key(name: str) -> Optional[str]:
    """
    Get an API key value by name.
    
    Args:
        name: The name of the API key
        
    Returns:
        The API key value, or None if not found
    """
    return get_key_manager().get_key(name)
