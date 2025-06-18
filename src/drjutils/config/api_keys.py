"""
API Key Management

Utilities for managing API keys stored in credential managers like Windows Credential Manager.
This module helps with retrieving API keys based on a standard configuration format.
Encrypts the cached keys, can only be used by calling the key() function.

Classes:
    ApiKey:     Represents an API key configuration
    ApiKeys:    Manages API keys based on a configuration file

Copyright 2025 Daniel Robert Jackson
"""

"""
Standard Libraries
"""
# Path manipulation
from pathlib    import Path
# Type hints
from typing     import Dict, List, Optional, Any


"""
Third-Party Libraries
"""
# Credential retrieval
try:
    import keyring
    KEYRING_AVAILABLE = True
except ImportError:
    KEYRING_AVAILABLE = False

"""
Local Libraries
"""
# Configuration loader
from ..configurator.loader  import ConfigLoader
from .                      import Files
# Logging
from ..logger               import debug, info, warning, error

class ApiKey:
    """
    Represents an API key stored in a credential manager.
    
    Attributes:
        name:           The name of the key in the config file
        service:        The service name in the credential manager
        username:       The username for the credential
        description:    A description of the key
        
    Methods:
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize an API key from a configuration dictionary.
        
        Args:
            config: The configuration dictionary for this key
        """
        assert KEYRING_AVAILABLE,'''\
            Keyring Library is not available
            Install keyring to use API keys:
            Run the command:
                poetry install keyring\
            '''
        
        self.name           = config.get('name')
        self.service        = config.get('service')
        self.username       = config.get('username')
        self.description    = config.get('description')
        
        # Validate the configuration
        assert self.name,       ValueError("API key configuration is missing the 'name' field")
        assert self.service,    ValueError(f"API key '{self.name}' is missing the 'service' field")
        assert self.username,   ValueError(f"API key '{self.name}' is missing the 'username' field")
    
    def key(self) -> Optional[str]:
        """
        Retrieve the API key value from the credential manager.
        
        Returns:
            The API key value
        
        Raises:
            ValueError: If the key is not found
        """
        key = keyring.get_password(self.service, self.username)
        if key is None:
            raise ValueError(f"No key found for {self}")
        return key
    
    def __str__(self) -> str:
        """Return a string representation of this API key."""
        return f"{self.name} (service: {self.service}, username: {self.username})"


class KeyManager:
    """
    Manages API keys based on a configuration file.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the key manager.
        
        Args:
            config_path: Path to the keys configuration file. If None,
                         attempts to find an api_keys.yaml file in standard locations.
        """
        self.keys: Dict[str, ApiKey] = {}
        self.config_path = config_path
        self._load_config()

    def _load_config(self):
        """
        Load configuration from YAML file.
        """
        # Find keys config if not provided
        config_path = self.config_path
        if config_path is None:
            config_path = find_api_keys_config()

            if config_path is None:
                warning("No api_keys.yaml found in standard locations")
                return

        self.config_path = config_path
        
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
        
        # Check for the keys array
        keys_list = config.get('keys')
        if not keys_list or not isinstance(keys_list, list):
            warning("No 'keys' array found in api_keys.yaml or invalid format")
            return
        
        # Process each key in the list
        for key_config in keys_list:
            try:
                # Skip any non-dictionary values
                if not isinstance(key_config, dict):
                    continue
                
                api_key = ApiKey(key_config)
                self.keys[api_key.name] = api_key
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


def get_package_config_path() -> Path:
    """
    Get the path to the template api_keys.yaml included in the package.
    
    Returns:
        Path to the template configuration file
    """
    return Path(__file__).parent / "api_keys.yaml"


def get_user_config_path() -> Path:
    """
    Get the path to the user's central api_keys.yaml.
    
    Returns:
        Path to the user's configuration file
    """
    return Path.home() / ".drjutils" / "api_keys.yaml"


def find_api_keys_config() -> Optional[str]:
    """
    Find an api_keys.yaml file in standard locations.
    
    Searches in the following order:
    1. Current directory and parent directories
    2. User's .drjutils directory
    3. Package template
    
    Returns:
        Path to the configuration file, or None if not found
    """
    from .utils import find_config_file
    
    # First, check the project directory and parent directories
    config_path = find_config_file("api_keys.yaml")
    if config_path is not None:
        debug(f"Found project api_keys.yaml: {config_path}")
        return config_path
    
    # Next, check the user's config directory
    user_path = get_user_config_path()
    if user_path.exists():
        debug(f"Found user api_keys.yaml: {user_path}")
        return str(user_path)
    
    # Finally, check the package template
    package_path = get_package_config_path()
    if package_path.exists():
        debug(f"Using package template api_keys.yaml: {package_path}")
        return str(package_path)
    
    # No config found
    return None


# Singleton instance of the key manager
_key_manager_instance = None

def get_key_manager(config_path: Optional[str] = None) -> KeyManager:
    """
    Get a KeyManager instance.
    
    Args:
        config_path: Path to the api_keys.yaml file
        
    Returns:
        A KeyManager instance
    """
    global _key_manager_instance
    
    # If a specific path is provided, create a new instance
    if config_path is not None:
        return KeyManager(config_path)
    
    # Otherwise, use the singleton instance
    if _key_manager_instance is None:
        _key_manager_instance = KeyManager()
    
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