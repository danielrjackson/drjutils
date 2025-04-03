"""
Schema Parser

Loads and parses configuration schemas with support for templates, constants,
and validators.

This module supports both nested and flat schema structures and handles
conversion between schema files and ConfigSchema objects.

Copyright 2025 Daniel Robert Jackson
"""

import re
import yaml
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

# Import local modules
from .schema import ConfigSchema, ConfigSchemaEntry

# Regular expression for range validator detection
RANGE_PATTERN = re.compile(r'^\s*(\S+)\s*\.\.\s*(\S+)\s*$')

class SchemaParser:
    """
    Parser for enhanced schema files with templates, constants, and validators.
    """
    
    def __init__(self):
        """Initialize the schema parser."""
        self.reset()
    
    def reset(self):
        """Reset the parser state."""
        self.constants = {}
        self.validators = {}
        self.templates = {}
        self.entries = []
    
    def parse_file(self, schema_path):
        """
        Parse a schema file.
        
        Args:
            schema_path: Path to the schema file
            
        Returns:
            A ConfigSchema instance
        """
        with open(schema_path, 'r') as f:
            schema_data = yaml.safe_load(f)
        
        return self.parse_dict(schema_data)
    
    def parse_dict(self, schema_data):
        """
        Parse a schema dictionary.
        
        Args:
            schema_data: Schema dictionary
            
        Returns:
            A ConfigSchema instance
        """
        # Reset the parser state
        self.reset()
        
        # Process sections in a specific order
        self._process_constants(schema_data.get('constants', {}))
        self._process_validators(schema_data.get('validators', {}))
        self._process_templates(schema_data.get('templates', {}))
        
        # Process the schema section (either flat or nested)
        schema_section = schema_data.get('schema', {})
        if schema_section:
            if 'schema_entries' in schema_data:
                # Flat format
                self._process_flat_schema(schema_data.get('schema_entries', []))
            else:
                # Nested format
                self._process_nested_schema(schema_section)
        
        # Create and return the ConfigSchema
        return ConfigSchema(self.entries)
    
    def _process_constants(self, constants):
        """
        Process the constants section.
        
        Args:
            constants: Dictionary of constants
        """
        for name, value in constants.items():
            self.constants[name] = value
    
    def _process_validators(self, validators):
        """
        Process the validators section.
        
        Args:
            validators: Dictionary of validators
        """
        for name, value in validators.items():
            self.validators[name] = self._resolve_value(value)
    
    def _process_templates(self, templates):
        """
        Process the templates section.
        
        Args:
            templates: Dictionary of templates
        """
        for name, template in templates.items():
            # Resolve any references in the template
            resolved_template = {}
            for key, value in template.items():
                resolved_template[key] = self._resolve_value(value)
            
            self.templates[name] = resolved_template
    
    def _process_flat_schema(self, schema_entries):
        """
        Process a flat schema format.
        
        Args:
            schema_entries: List of schema entries
        """
        for entry_data in schema_entries:
            entry = self._create_entry_from_dict(entry_data)
            if entry:
                self.entries.append(entry)
    
    def _process_nested_schema(self, schema_section, parent_path=None):
        """
        Process a nested schema format recursively.
        
        Args:
            schema_section: Dictionary for this section of the schema
            parent_path: Parent path for nested keys
        """
        for key, value in schema_section.items():
            current_path = [key] if parent_path is None else parent_path + [key]
            
            # Check if this is a leaf node (has format or template)
            if 'format' in value or 'template' in value:
                # Create entry for this leaf
                entry_data = {'name': key, 'path': current_path}
                entry_data.update(value)
                entry = self._create_entry_from_dict(entry_data)
                if entry:
                    self.entries.append(entry)
            else:
                # Recurse into this section
                self._process_nested_schema(value, current_path)
    
    def _create_entry_from_dict(self, entry_data):
        """
        Create a ConfigSchemaEntry from a dictionary.
        
        Args:
            entry_data: Dictionary with entry data
            
        Returns:
            A ConfigSchemaEntry instance
        """
        # Handle template references
        if 'template' in entry_data:
            template_name = entry_data['template']
            if template_name in self.templates:
                # Start with template, override with entry data
                template = self.templates[template_name].copy()
                
                # Remove the template reference
                entry_data = entry_data.copy()
                del entry_data['template']
                
                # Override template with entry-specific values
                template.update(entry_data)
                entry_data = template
            else:
                raise ValueError(f"Template not found: {template_name}")
        
        # Get required fields
        name = entry_data.get('name')
        if not name:
            raise ValueError("Schema entry must have a name")
        
        # Get path (list of keys or string)
        path = entry_data.get('path')
        if isinstance(path, str):
            # Handle array notation in path string
            if '[]' in path:
                parts = []
                for part in path.split('.'):
                    if part.endswith('[]'):
                        parts.append(part[:-2])
                        parts.append('[]')
                    else:
                        parts.append(part)
                path = parts
            else:
                path = path.split('.')
        
        # If path is still None, use the name
        if path is None:
            path = [name]
        
        # Get the format type
        format_type = self._resolve_format(entry_data.get('format'))
        
        # Resolve other fields
        default = self._resolve_value(entry_data.get('default'))
        validator = self._resolve_validator(entry_data.get('validator'), format_type)
        nullable = entry_data.get('nullable', True)
        required = entry_data.get('required', True)
        
        # Create the entry
        return ConfigSchemaEntry(
            name=name,
            path=path,
            format_type=format_type,
            default=default,
            validator=validator,
            nullable=nullable,
            required=required
        )
    
    def _resolve_value(self, value):
        """
        Resolve a value, processing any references to constants.
        
        Args:
            value: The value to resolve
            
        Returns:
            The resolved value
        """
        if isinstance(value, str) and value.startswith('$'):
            # This is a reference to a constant
            constant_name = value[1:]
            if constant_name in self.constants:
                return self.constants[constant_name]
            else:
                raise ValueError(f"Constant not found: {constant_name}")
        return value
    
    def _resolve_format(self, format_str):
        """
        Resolve a format string to a Python type.
        
        Args:
            format_str: String representation of the type
            
        Returns:
            The corresponding Python type
        """
        if not format_str:
            return None
        
        # Map format strings to types
        format_map = {
            'bool': bool,
            'bytes': bytes,
            'datetime': datetime,
            'float': float,
            'int': int,
            'str': str,
            'Dict': dict,
            'List': list,
            'Path': Path
        }
        
        return format_map.get(format_str)
    
    def _resolve_validator(self, validator, format_type):
        """
        Resolve a validator, handling references and ranges.
        
        Args:
            validator: The validator to resolve
            format_type: The format type for this entry
            
        Returns:
            The resolved validator
        """
        # Resolve any references
        validator = self._resolve_value(validator)
        
        if validator is None:
            return None
        
        # Check for range notation (e.g., [1..100])
        if isinstance(validator, str):
            match = RANGE_PATTERN.match(validator)
            if match:
                start, end = match.groups()
                
                # Convert range values based on format type
                if format_type in (int, float):
                    try:
                        if format_type == int:
                            start = int(start)
                            end = int(end)
                        else:
                            start = float(start)
                            end = float(end)
                        return (start, end)
                    except ValueError:
                        raise ValueError(f"Invalid range values for {format_type.__name__}: {start}..{end}")
                else:
                    # String or other type range
                    return (start, end)
            
            # Handle regex for strings
            if format_type == str:
                try:
                    return re.compile(validator)
                except re.error as e:
                    raise ValueError(f"Invalid regex pattern: {validator}, error: {str(e)}")
        
        # Handle explicit range notation [start..end]
        elif isinstance(validator, list) and len(validator) == 1 and isinstance(validator[0], str):
            range_str = validator[0]
            match = RANGE_PATTERN.match(range_str)
            if match:
                start, end = match.groups()
                
                # Convert range values based on format type
                if format_type in (int, float):
                    try:
                        if format_type == int:
                            start = int(start)
                            end = int(end)
                        else:
                            start = float(start)
                            end = float(end)
                        return (start, end)
                    except ValueError:
                        raise ValueError(f"Invalid range values for {format_type.__name__}: {start}..{end}")
                else:
                    # String or other type range
                    return (start, end)
        
        return validator

# Convenience function to parse a schema file
def parse_schema_file(schema_path):
    """
    Parse a schema file.
    
    Args:
        schema_path: Path to the schema file
        
    Returns:
        A ConfigSchema instance
    """
    parser = SchemaParser()
    return parser.parse_file(schema_path)

# Convenience function to parse a schema dictionary
def parse_schema_dict(schema_dict):
    """
    Parse a schema dictionary.
    
    Args:
        schema_dict: Schema dictionary
        
    Returns:
        A ConfigSchema instance
    """
    parser = SchemaParser()
    return parser.parse_dict(schema_dict)
