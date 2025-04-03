"""
Configuration Class Generators

Generates Python classes from configuration schemas for type-safe configuration access.

This module provides functions to convert ConfigSchema objects into Python classes
that provide typed properties, validation, and structured access to configuration data.

Copyright 2025 Daniel Robert Jackson
"""

import re
import inspect
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple, Type, Union, get_type_hints

from .schema import ConfigSchema, ConfigSchemaEntry

class SchemaClassGenerator:
    """
    Generates Python classes from configuration schemas.
    """
    
    def __init__(self, schema: ConfigSchema):
        """
        Initialize the class generator.
        
        Args:
            schema: The schema to generate classes from
        """
        self.schema = schema
        self.generated_classes = {}
        self.path_prefixes = self._get_path_prefixes()
        
    def _get_path_prefixes(self):
        """
        Get all unique path prefixes from the schema entries.
        
        This identifies nested objects that need their own classes.
        
        Returns:
            A set of path prefixes
        """
        prefixes = set()
        for entry in self.schema.entries.values():
            path = entry.path
            if isinstance(path, str):
                path = path.split('.')
                
            # Add each prefix up to the parent
            for i in range(1, len(path)):
                prefixes.add(tuple(path[:i]))
        
        return prefixes
    
    def _analyze_paths(self):
        """
        Analyze paths to determine class structure.
        
        Returns:
            A dictionary mapping path prefixes to their entries
        """
        # Group entries by their parent paths
        path_entries = {}
        for entry in self.schema.entries.values():
            path = entry.path
            if isinstance(path, str):
                path = path.split('.')
                
            # Skip array notation paths for now (handled separately)
            if any(p == '[]' for p in path):
                continue
                
            # Get the parent path
            if len(path) > 1:
                parent = tuple(path[:-1])
                if parent not in path_entries:
                    path_entries[parent] = []
                path_entries[parent].append(entry)
        
        return path_entries
    
    def _analyze_array_items(self):
        """
        Analyze array items to determine item classes.
        
        Returns:
            A dictionary mapping array paths to their item entries
        """
        # Find array item entries
        array_items = {}
        for entry in self.schema.entries.values():
            path = entry.path
            if isinstance(path, str):
                path = path.split('.')
                
            # Check for array notation
            array_indices = [i for i, p in enumerate(path) if p == '[]']
            if array_indices:
                # Get the array path (up to the array marker)
                array_idx = array_indices[0]
                array_path = tuple(path[:array_idx])
                
                # Skip if this is a nested array item
                if len(array_indices) > 1:
                    continue
                    
                # Get the item entry
                item_path = path[array_idx+1:]
                if array_path not in array_items:
                    array_items[array_path] = []
                    
                # Store with the remaining path
                array_items[array_path].append((item_path, entry))
        
        return array_items
    
    def generate_classes(self, base_name="Config"):
        """
        Generate Python classes from the schema.
        
        Args:
            base_name: Base name for the root config class
            
        Returns:
            The root config class
        """
        # Analyze paths and arrays
        path_entries = self._analyze_paths()
        array_items = self._analyze_array_items()
        
        # Generate classes from the bottom up (leaf classes first)
        sorted_paths = sorted(path_entries.keys(), key=len, reverse=True)
        
        # Generate array item classes first
        for array_path, items in array_items.items():
            if items:
                class_name = self._path_to_class_name(array_path) + "Item"
                self._generate_class(class_name, items, is_array_item=True)
        
        # Generate regular classes
        for path in sorted_paths:
            class_name = self._path_to_class_name(path)
            entries = path_entries[path]
            self._generate_class(class_name, entries)
        
        # Generate the root class
        root_entries = path_entries.get((), [])
        root_class = self._generate_class(base_name, root_entries, is_root=True)
        
        return root_class
    
    def _path_to_class_name(self, path):
        """
        Convert a path to a class name.
        
        Args:
            path: Path tuple or list
            
        Returns:
            A class name
        """
        if not path:
            return "RootConfig"
            
        # Capitalize each path component
        parts = [p.capitalize() for p in path]
        return ''.join(parts) + "Config"
    
    def _generate_class(self, class_name, entries, is_array_item=False, is_root=False):
        """
        Generate a class for a specific path.
        
        Args:
            class_name: Name for the class
            entries: List of entries for this class
            is_array_item: Whether this is an array item class
            is_root: Whether this is the root config class
            
        Returns:
            The generated class
        """
        # Check if already generated
        if class_name in self.generated_classes:
            return self.generated_classes[class_name]
        
        # Dictionary to hold class attributes
        class_attrs = {}
        
        # Track nested objects
        nested_objects = {}
        
        # Process regular entries
        for entry in entries:
            # Skip if this is an array item class and the entry is not for an item
            if is_array_item:
                # Handle the item path
                pass
            
            # Get entry properties
            name = entry.name
            format_type = entry.format_type
            default = entry.default
            validator = entry.validator
            nullable = entry.nullable
            required = entry.required
            
            # Add the private attribute
            class_attrs[f"_{name}"] = None
            
            # Add the property getter
            def make_getter(name):
                return property(lambda self: getattr(self, f"_{name}"))
            
            # Add the property setter (with validation)
            def make_setter(name, format_type, validator, nullable, required):
                def setter(self, value):
                    # Validate the value
                    if value is None:
                        if not nullable:
                            raise ValueError(f"{name} cannot be None")
                    elif format_type and not isinstance(value, format_type):
                        raise TypeError(f"{name} must be of type {format_type.__name__}")
                        
                    # Apply validator if present
                    if validator and value is not None:
                        if isinstance(validator, tuple) and len(validator) == 2:
                            # Range validator
                            min_val, max_val = validator
                            if value < min_val or value > max_val:
                                raise ValueError(f"{name} must be between {min_val} and {max_val}")
                        elif hasattr(validator, 'match') and callable(getattr(validator, 'match')):
                            # Regex validator
                            if not validator.match(str(value)):
                                raise ValueError(f"{name} does not match pattern: {validator.pattern}")
                        elif isinstance(validator, list):
                            # List of allowed values
                            if value not in validator:
                                raise ValueError(f"{name} must be one of: {validator}")
                        elif callable(validator):
                            # Custom validator function
                            result = validator(value)
                            if result is False:
                                raise ValueError(f"{name} failed validation")
                    
                    # Set the value
                    setattr(self, f"_{name}", value)
                    
                return property(lambda self: getattr(self, f"_{name}"), setter)
            
            # Create the property
            class_attrs[name] = make_setter(name, format_type, validator, nullable, required)
        
        # Add initialization method
        def __init__(self, config_dict=None):
            if config_dict is None:
                config_dict = {}
                
            # Set attributes from config
            for key, value in config_dict.items():
                if hasattr(self, f"_{key}"):
                    # Check for nested objects
                    if isinstance(value, dict) and hasattr(self, f"_{key}_class"):
                        nested_class = getattr(self, f"_{key}_class")
                        setattr(self, f"_{key}", nested_class(value))
                    elif isinstance(value, list) and hasattr(self, f"_{key}_item_class"):
                        # Handle list of items
                        item_class = getattr(self, f"_{key}_item_class")
                        items = []
                        for item in value:
                            if isinstance(item, dict):
                                items.append(item_class(item))
                            else:
                                items.append(item)
                        setattr(self, f"_{key}", items)
                    else:
                        # Set the value directly
                        setattr(self, key, value)
        
        # Add string representation
        def __str__(self):
            attrs = []
            for key in self.__dict__:
                if key.startswith('_') and not key.endswith('_class') and not key.endswith('_item_class'):
                    attr_name = key[1:]
                    value = getattr(self, key)
                    attrs.append(f"{attr_name}={value}")
            return f"{self.__class__.__name__}({', '.join(attrs)})"
        
        # Add representation
        def __repr__(self):
            return self.__str__()
        
        # Add methods to class attributes
        class_attrs['__init__'] = __init__
        class_attrs['__str__'] = __str__
        class_attrs['__repr__'] = __repr__
        
        # Create the class
        cls = type(class_name, (), class_attrs)
        
        # Store in generated classes
        self.generated_classes[class_name] = cls
        
        return cls

# Convenience function to generate classes from a schema
def generate_config_classes(schema, base_name="Config"):
    """
    Generate Python classes from a schema.
    
    Args:
        schema: ConfigSchema instance
        base_name: Base name for the root config class
        
    Returns:
        The root config class
    """
    generator = SchemaClassGenerator(schema)
    return generator.generate_classes(base_name)
