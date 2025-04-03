"""
Configuration Utilities

Utility functions for working with configuration files.

Functions:
    merge_configs: Merge two configuration dictionaries
    find_config_file: Find a configuration file in common locations
    generate_sample_config: Generate a sample configuration from a schema

Copyright 2025 Daniel Robert Jackson
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

def merge_configs(base_config: Dict[str, Any], override_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively merge two configuration dictionaries.
    
    The override_config takes precedence over the base_config.
    
    Args:
        base_config: The base configuration dictionary
        override_config: The configuration dictionary with overrides
        
    Returns:
        The merged configuration dictionary
    """
    result = base_config.copy()
    
    for key, value in override_config.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            # If both values are dictionaries, merge them recursively
            result[key] = merge_configs(result[key], value)
        else:
            # Otherwise, override the value
            result[key] = value
    
    return result

def find_config_file(config_name: str, search_paths: Optional[List[Union[str, Path]]] = None) -> Optional[Path]:
    """
    Find a configuration file in common locations.
    
    Args:
        config_name: The name of the configuration file
        search_paths: Additional paths to search
        
    Returns:
        The path to the configuration file, or None if not found
    """
    if search_paths is None:
        search_paths = []
    
    # Add default search paths
    search_paths = search_paths + [
        Path.cwd(),
        Path.cwd() / "config",
        Path.home(),
        Path.home() / ".config"
    ]
    
    # Search for the configuration file
    for path in search_paths:
        config_path = Path(path) / config_name
        if config_path.exists():
            return config_path
    
    return None

def generate_sample_config(schema, include_comments: bool = True) -> Dict[str, Any]:
    """
    Generate a sample configuration dictionary from a schema.
    
    Args:
        schema: The schema to generate the sample from
        include_comments: Whether to include comments in the sample
        
    Returns:
        A sample configuration dictionary
    """
    sample = {}
    
    # Get all entries from the schema
    entries = schema.entries.values()
    
    # Group entries by their first path component
    groups = {}
    for entry in entries:
        path = entry.path
        if not path:
            continue
        
        first_key = path[0]
        if first_key not in groups:
            groups[first_key] = []
        
        groups[first_key].append(entry)
    
    # Build the sample configuration
    for group_key, group_entries in groups.items():
        # Create a sub-dictionary for the group
        sample[group_key] = {}
        
        # Add entries for the group
        for entry in group_entries:
            # For nested paths, we need to build the structure recursively
            current = sample[group_key]
            for key in entry.path[1:-1]:
                if key not in current:
                    current[key] = {}
                current = current[key]
            
            # Add the leaf value
            leaf_key = entry.path[-1]
            
            # Use default value if available, otherwise generate a sample value
            if entry.default is not None:
                current[leaf_key] = entry.default
            else:
                current[leaf_key] = _generate_sample_value(entry)
    
    return sample

def _generate_sample_value(entry):
    """
    Generate a sample value for a schema entry.
    
    Args:
        entry: The schema entry to generate a sample value for
        
    Returns:
        A sample value appropriate for the entry
    """
    if entry.format_type == str:
        return f"sample_{entry.name}"
    elif entry.format_type == int:
        return 42
    elif entry.format_type == float:
        return 3.14
    elif entry.format_type == bool:
        return True
    elif entry.format_type == list:
        return []
    elif entry.format_type == dict:
        return {}
    elif entry.format_type == Path:
        return str(Path.cwd() / entry.name)
    else:
        return None