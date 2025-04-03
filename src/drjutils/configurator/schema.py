"""
Configuration Schema

Contains classes for generating and validating configuration schemas and files.

Classes:
    ConfigSchema: Validates a configuration dictionary
    ConfigSchemaEntry: An entry in a configuration schema

Copyright 2025 Daniel Robert Jackson
"""

"""
Standard Libraries
"""
from base64     import  b64encode, b64decode
from datetime   import  datetime
from enum       import  Enum
from pathlib    import  Path
from typing     import  Any, Dict, List, Optional, Tuple, Union, Callable
from re         import  Pattern, compile, match, search, split

"""
Third-Party Libraries
"""
# Interval arithmetic
from sympy      import  Interval
# YAML parsing
import yaml

"""
Local Libraries
"""
try:
    from drjutils.logger import debug
except ImportError:
    # If the logger module is not available, use the standard library logger
    from logging import debug

class ConfigSchemaEntry:
    """
    An entry in a configuration schema.
    
    Defines validation rules for a single configuration entry.
    
    Properties:
        name:       Name of the entry (last path key)
        path:       Dictionary path to the entry (list of keys)
        format:     Data type or encoding (See below for supported types; allows multiple types to be specified)
        default:    Default value for the entry
        validator:  Validator for the entry.
        nullable:   Whether None is allowed as a value
        required:   Whether the entry must be present in the configuration
        children:   Sub-entries for container types (Dict, List) (Single ConfigSchemaEntry for List, Dict of ConfigSchemaEntry for Dict)
    
    Private Properties:
        __default_property_values:  A dictionary that replaces the default assumptions for the entry properties.
        
    
    Default Property Values (if not provided or overridden):
        (Must provide at least one of name or path)
        name:       Can be inferred from last path key
        path:       Can be inferred to be just the name
        format:     Can be inferred from default or validator
        default:    None (if nullable) or inferred from format
        validator:  Can be inferred from format and/or default
        nullable:   True
        required:   True
        children:   Must be None (for non-container types); must be defined (for container types)
        
    
    Supported formats:
        - basic types:
            - bool
            - bytes
                - Encoding: (interpretation of bytes)
                    - base64
                    - hex
                    - binary
            - datetime
            - float
            - int
            - str
        - container types: (will be validated recursively)
            - Dict
            - List
        - special types:
            - Enum (must provide full import path or define the Enum in the config file)
            - Interval
            - Path
            - Pattern
            - Tuple
    
    
    Validator instructions:
        A validator should be a callable that takes a single argument and returns a boolean.
        Some other types are supported and will automatically be converted to a callable:
            - Interval: A range of valid values
            - Pattern:  A regular expression that the value must match
            - Tuple:    A tuple of (min, max) (inclusive) values for numerical ranges
            - Enum:     An enumeration of valid values
            - List:     A list of valid values
            - str:      Interpreted based on the format and if it matches expected styles for initializing one of the above types
            

    """
    __UNSPEC = object()
        
    class Props(Enum):
        """
        Configuration schema entry properties.
        """
        NAME        = "name"
        PATH        = "path"
        FORMAT      = "format"
        DEFAULT     = "default"
        VALIDATOR   = "validator"
        NULLABLE    = "nullable"
        REQUIRED    = "required"
    
    # Regular expressions for validation
    __key_delim_list    = [" ", "\t", ".", ",", "|", "/", "\\"]
    __key_delims        = f"[.,|/\\]"
    __all_key_delims    = r"[ \t.,|/\\]" # Includes empty delimiters
    __key_str           = f"[\w-]*"
    __b64_elem          = f"[a-z\d+/]"
    
    class __Rx:
        """
        Regular expressions for validation.
        """
        hex       = compile(r"(?i)^(?:0x)?([a-f\d]+)$")
        b64       = compile(r"(?i)^(?:[a-z\d+/]{4})+(?:[a-z\d+/]{3}=|[a-z\d+/]{2}==)$")
        key       = compile(r"(?i)^[\w-]*$")
        cfg_path  = compile(r"(?i)^[\w-]*(?:[ \t.,|/\\][\w-]*)*$")
    
    # Used to reset the default values for the properties    
    __original_default_property_values = {
        Props.FORMAT:       None,
        Props.DEFAULT:      __UNSPEC,
        Props.VALIDATOR:    None,
        Props.NULLABLE:     True,
        Props.REQUIRED:     True
    }
    
    __default_property_values = __original_default_property_values.copy()
    
    class Format(Enum):
        """
        Supported formats for configuration entries.
        """
        BOOL        = "bool"
        BYTES       = "bytes"
        BASE64      = "base64"
        HEX         = "hex"
        BINARY      = "binary"
        DATETIME    = "datetime"
        FLOAT       = "float"
        INT         = "int"
        STR         = "str"
        DICT        = "dict"
        ENUM        = "enum",
        INTERVAL    = "interval"
        LIST        = "list"
        PATH        = "path"
        PATTERN     = "pattern"
        TUPLE       = "tuple"
        
        def type(self):
            """
            Get the type for the format.
            """
            # switch statement
            return {
                self.BOOL:       bool,
                self.BYTES:      bytes,
                self.BASE64:     bytes,
                self.HEX:        bytes,
                self.BINARY:     bytes,
                self.DATETIME:   datetime,
                self.FLOAT:      float,
                self.INT:        int,
                self.STR:        str,
                self.DICT:       dict,
                self.ENUM:       Enum,
                self.INTERVAL:   Interval,
                self.LIST:       list,
            }[self]
    
    def __init__(self,
                 name:      Optional[str]                                                                       = None,
                 path:      Optional[Union[List[str], str]]                                                     = None,
                 format:    Optional[Union[Format, type, str, List[Union[Format, type, str]]]]                  = None,
                 default:   Optional[Any]                                                                       = __UNSPEC,
                 validator: Optional[Union[Callable, Interval, Pattern, Tuple[int, float], Enum, List, str]]    = None,
                 nullable:  Optional[bool]                                                                      = None,
                 required:  Optional[bool]                                                                      = None,
                 template:  Optional[Union[Dict[Props, Any], Dict[str, Any]]]                                   = None,
                 ):
        """
        Initialize the configuration schema entry.
        
        Either a name or a path must be provided.
        Either a format or a default must be provided.
        
        Note that for the types, they are ordered by preferred interpretation.
        
        Args:
            name:       Name of the entry (last path key)
            path:       Dictionary path to the entry (list of keys or delimited string)
            format:     Data type or encoding (e.g., str, int, float, bool, Path; allows multiple types to be specified)
            default:    Default value for the entry
            validator:  Validator for the entry (range, regex, function)
            nullable:   Whether None is allowed as a value
            required:   Whether the entry must be present in the configuration
            template:   A dictionary of default values for the entry properties
        """
        # The name or path must be provided and can't be derived from a template.
        self.name       = name
        self.path       = path
        
        
        template = self.__gen_template(template)
        
        # Initialize with defaults
        self.format     = template.get("format",    format)
        self.default    = template.get("default",   default)
        self.validator  = template.get("validator", validator)
        self.nullable   = template.get("nullable",  nullable)
        self.required   = template.get("required",  required)
        
        if format is not None:
            self.format = format
        if default is not __UNSPEC:
            self.default = default
        if validator is not None:
            self.validator = validator
        if nullable is not None:
            self.nullable = nullable
        if required is not None:
            self.required = required
        
        # Clean up and validate the entry
        self.clean()
    
    def clean(self):
        """
        Fix any inferable issues with the configuration entry.
        
        Useful to call if any of the fields are modified after initialization.
        Does not fix conflicts between fields, just fills in missing values.
        
        Raises:
            ValueError: If the configuration entry is invalid
        """
        # Resolution phase - fills in missing values
        self.__resolve_name_and_path()
        self.__resolve_format_and_default()
        self.__resolve_validator()
        
        # Validation phase - ensures everything is valid
        self.__validate_self()
    
    def interpret_value(self,
                        value,
                        format: Optional[Union[Format, type, str, List[Union[Format, type, str]]]] = None)
        """
        Interpret a value based on the format.
        
        Args:
            value: The value to interpret
            format: The format to interpret the value as (optional)
        
        Returns:
            The interpreted value
        """
        # Sanity check that self.format is not None and has been processed
        if self.format is None:
            raise ValueError("ConfigSchemaEntry format cannot be None")
        elif self.format is not isinstance(self.Format):
            __resolve_format()
        
        # Check that the passed format is valid
        if format is not None:
            if not isinstance(format, (type, str, list)):
                raise TypeError(f"Invalid ConfigSchemaEntry format: {format}; expected type, str, or list")
        
        # Handle the case where the value is None
        if value is None:
            if not self.nullable:
                raise ValueError(f"{self.name} cannot be None")

            value = self.default
        elif isinstance(self.format, list):
            # If the format property is a list, then it could be one of several formats.
            # We need to determine which of the possible types most closely matches the value
            # We will then re-call this function with the determined format
            # The formats should be ordered by preference
            # First check to see if we've already determined the format
            if format is None:
                for possible_format in self.format:
                    try:
                        return self.interpret_value(value, possible_format)
                    except ValueError:
                        pass
        elif isinstance(self.format, self.Encoding):
            # If the format is an encoding, we need to interpret the value
            value = self._interpret_single_value(value)
        elif self.format == Path:
            if isinstance(value, str):
                value = Path(value)

            # Ensure that the path is absolute
            if not value.is_absolute():
                value = Path.absolute(value)
        elif self.format == bool:
            if isinstance(value, str):
                value = value.lower()
                if   value in ("true", "yes", "on"):
                    value = True
                elif value in ("false", "no", "off"):
                    value = False
                else:
                    raise ValueError(f"Invalid boolean value: {value}")
        elif self.format == list:
            if isinstance(value, str):
                value = value.split(",")
        elif self.format == dict:
            if isinstance(value, str):
                value = yaml.safe_load(value)
        elif self.format == bytes:
            if isinstance(value, str):
        
        return value
    
    def override_defaults(self, overrides):
        """
        Override the default values for all configuration entry properties.
        Only changes the properties specified in the overrides dictionary.
        
        Args:
            overrides: A dictionary of property names to new values
        """
        for key, value in overrides.items():
            if key not in self.default_property_values:
                raise ValueError(f"Invalid ConfigSchemaEntry property: {key}={value}")    
            
            # Check that the override is valid
            if not isinstance(value, (type, str, list)):
                valid
                raise TypeError(f"Invalid ConfigSchemaEntry format: {value}; expected bool, bytes, Encoding[base64, hex, binary], datetime, float, int, str, Dict, Enum, List, Path, Pattern, Tuple")

            if key == "format":
                if isinstance(value, list):
                    for possible_format in value:
                        interpret_format(possible_format)
                else:
                    interpret_format(value)
            elif key == "validator":
                if not isinstance(value, (Callable, Interval, Pattern, Tuple, Enum, List, str)):
                    raise TypeError(f"Invalid ConfigSchemaEntry validator: {value}; expected Callable, Interval, Pattern, Tuple, Enum, List, or str")
            elif key == "nullable":
                if not isinstance(value, bool):
                    raise TypeError(f"Invalid ConfigSchemaEntry nullable: {value}; expected bool")
            elif key == "required":
                if not isinstance(value, bool):
                    raise TypeError(f"Invalid ConfigSchemaEntry required: {value}; expected bool")
            
            self.default_property_values[key] = value
            
            setattr(self, key, value)
                    
    
    def __gen_template(self,
                       template: Optional[Dict[str, Any]]
                       ) -> Dict[str, Any]:
        """
        Generate a template dictionary for the configuration entry.
        
        Uses the default property values and fills in any missing values from the template.
        
        Args:
            template: A dictionary of default values for the entry properties
        
        Returns:
            A dictionary with the template values filled in
        """
        # Fill in missing template values
        resulting_template = self.__default_property_values.copy()
        
        if template is not None:
            for key, value in template.items():
                resulting_template[key] = value
        
        return resulting_template
    
    def __resolve_name_and_path(self):
        """
        Resolve the name and/or path for the configuration entry.
        
        If a name is provided, it will be used as the name.
        If a name is not provided, the last element of the path will be used as the name.
        If a path is provided, it will be used (or split) as the path.
        If a path is not provided, the name will be used as the path.
        
        Raises:
            ValueError: If neither name nor path is defined
        """
        # Check that either name or path is defined
        if self.name is None and self.path is None:
            raise ValueError("Either name or path must be defined")
        
        # Convert path to a list if it's a string
        if isinstance(self.path, str):
            if search(self.empty_delimiters, self.path):
                self.path = self.path.split()
            else:
                self.path = split(self.key_delimiters, self.path)
        
        # Infer name from path if not provided
        if self.name is None and self.path is not None:
            self.name = self.path[-1]
        
        # Infer path from name if not provided
        if self.path is None and self.name is not None:
            self.path = [self.name]
    
    def __resolve_format(self):
        """
        Resolve the format for the configuration entry.
        
        If format is not provided, infer it from the default value or validator.
        
        Raises:
            ValueError: If the format cannot be inferred
        """
        if self.format is None and self.default is None and self.validator is None:
            raise ValueError(f"Cannot infer format from missing default value for {self.name}")
            
        if self.format is None:
            if self.default is not None:
                self.format = type(self.default)
                debug(f"ConfigSchemaEntry::{self.name}: Inferred format ({self.format}) from default value ({type(self.default)}:{self.default}).")
            elif self.validator is not None:
                if isinstance(self.validator, Pattern):
                    self.format = str
                    debug(f"ConfigSchemaEntry::{self.name}: Inferred format ({self.format}) from validator ({type(self.validator)}:{self.validator}).")
                elif isinstance(self.validator, tuple) and len(self.validator) == 2:
                    if all(isinstance(val, int) for val in self.validator):
                        self.format = int
                    elif all(isinstance(val, float) for val in self.validator):
                        self.format = float
                    else:
                        raise ValueError(f"Cannot infer format from invalid validator for {self}")
                elif isinstance(self.validator, Callable):
                    self.format = self.validator
                else:
                    raise ValueError(f"Cannot infer format from validator for {self.name}")
            self.format = type(self.default)
    
    def __resolve_format_and_default(self):
        """
        Resolve the format and default value for the configuration entry.
        
        If format is not provided, infer it from the default value.
        If default is not provided and the entry is not nullable, generate a default value.
        
        Raises:
            ValueError: If neither format nor default is provided
        """
        # If neither format nor default is provided, we can't proceed
        if self.format is None and self.default is None:
            raise ValueError(f"Either format or default must be defined for {self.name}")
        
        # If format is not provided, infer it from the default value
        if self.format is None:
            self.format = type(self.default)
        
        # If default is not provided and the entry is not nullable, generate a default value
        if self.default is None and self.nullable is False:
            self.default = self.__generate_default()
    
    def __resolve_validator(self):
        """
        Resolve the validator for the configuration entry.
        
        If a validator is not provided, generate one based on the format.
        """
        if self.validator is None:
            self.__generate_validator()

        # Ensure that validator can be directly called and the stored value can just be passed directly to it
        # The default types that need to be handled are:
        #   - Pattern: str or Pattern
        #   - Tuple: int or float
        #   - Callable: function (already callable)
        if not isinstance(self.validator, Callable) and self.validator is not None:
            if isinstance(self.validator, Pattern):
                self.validator = self.validator.match
            elif isinstance(self.validator, tuple) and len(self.validator) == 2:
                self.validator = self.validator
            else:
                raise TypeError(f"Validator must be a callable, got {type(self.validator)}:{self.validator}")
            
            
    
    def __validate_self(self):
        """
        Validate that this configuration schema entry is correctly initialized.
        """
        # Validate name
        if self.name is None:
            raise ValueError("Name must be defined")
        
        if not isinstance(self.name, str):
            raise TypeError(f"Name must be a string, got {type(self.name)}")
        
        if not match(self.yaml_key_regex, self.name):
            raise ValueError(f"Name must be a valid YAML key: {self.name}")
        
        # Validate path
        if self.path is None:
            raise ValueError("Path must be defined")
        
        if not isinstance(self.path, list):
            raise TypeError(f"Path must be a list, got {type(self.path)}")
        
        if not all(isinstance(key, str) for key in self.path):
            raise TypeError("All path elements must be strings")
        
        # Validate format
        if self.format is None:
            raise ValueError("Format must be defined")
        
        # Basic validation of default value against format
        if self.default is not None:
            self.__validate_default_against_format()
    
    def __validate_default_against_format(self):
        """
        Validate that the default value matches the specified format.
        """
        if self.default is None:
            if not self.nullable:
                raise ValueError(f"Default value for {self.name} cannot be None when nullable is False")
            return
        
        # Check if default matches format
        if not isinstance(self.default, self.format):
            # Special case for float/int compatibility
            if self.format == float and isinstance(self.default, int):
                self.default = float(self.default)
            else:
                raise TypeError(f"Default value for {self.name} must be a {self.format}, got {type(self.default)}")
    
    def __generate_default(self):
        """
        Generate a default value based on the format.
        
        Returns:
            A default value appropriate for the format
        """
        if self.format == str:
            return ""
        elif self.format == int:
            return 0
        elif self.format == float:
            return 0.0
        elif self.format == bool:
            return False
        elif self.format == list:
            return []
        elif self.format == dict:
            return {}
        elif self.format == Path:
            return Path.cwd()
        else:
            return None
    
    def __generate_validator(self):
        """
        Generate a validator based on the format.
        
        Sets self.validator to an appropriate validator for the format.
        """
        # Only generate if validator is not provided
        if self.validator is not None:
            return
        
        if self.format == str:
            # Default validator for strings: any string
            self.validator = compile(".*")
        elif self.format == int:
            # Default validator for integers: any integer
            self.validator = (-int('inf'), int('inf'))
        elif self.format == float:
            # Default validator for floats: any float
            self.validator = (-float('inf'), float('inf'))
        elif self.format == datetime:
            # Handle case where the date is a string and needs to be parsed.
        # Other types don't get default validators
    
    def validate(self, value):
        """
        Validate a value against this schema entry.
        
        Args:
            value: The value to validate
            
        Returns:
            The validated value (possibly converted to the correct type)
            
        Raises:
            ValueError: If the value is invalid
            TypeError: If the value is of the wrong type
        """
        # Check for None
        if value is None:
            if not self.nullable:
                raise ValueError(f"{self.name} cannot be None")
            return None
        
        # Check type
        if not isinstance(value, self.format):
            # Special case for float/int compatibility
            if self.format == float and isinstance(value, int):
                value = float(value)
            else:
                raise TypeError(f"{self.name} must be a {self.format}, got {type(value)}")
        
        # Apply validator if specified
        if self.validator is not None:
            if self.format == str and isinstance(self.validator, Pattern):
                # String validation with regex
                if not self.validator.match(value):
                    raise ValueError(f"{self.name} does not match pattern: {self.validator.pattern}")
            elif (self.format in (int, float)) and isinstance(self.validator, tuple) and len(self.validator) == 2:
                # Number validation with range
                min_val, max_val = self.validator
                if value < min_val or value > max_val:
                    raise ValueError(f"{self.name} must be between {min_val} and {max_val}")
            elif callable(self.validator):
                # Custom validation function
                result = self.validator(value)
                if result is False:
                    raise ValueError(f"{self.name} failed custom validation")
                if result is not True and result is not None:
                    # Validator returned a modified value
                    value = result
        
        return value
    
    def get_path_str(self):
        """
        Get a string representation of the path.
        
        Returns:
            str: A dot-separated string of the path keys
        """
        return ".".join(self.path)
    
    def __str__(self):
        """
        Get a string representation of this schema entry.
        
        Returns:
            str: A string representation of this schema entry
        """
        return f"{self.get_path_str()} ({self.format.__name__})"


class ConfigSchema:
    """
    Validates a configuration dictionary.
    
    Manages a collection of ConfigSchemaEntry objects and provides methods
    for validating configuration dictionaries against them.
    """
    
    def __init__(self,
                 entries=None,
                 source_config=None):
        """
        Initialize the configuration schema.
        
        Args:
            entries: A list of ConfigSchemaEntry objects or a dictionary mapping paths to entries
            source_config: A source configuration dictionary to automatically build a schema from
        """
        self.entries = {}
        
        if entries is not None:
            self.add_entries(entries)
        
        if source_config is not None and not self.entries:
            self.build_from_config(source_config)
    
    def add_entry(self, entry):
        """
        Add a single entry to the schema.
        
        Args:
            entry: A ConfigSchemaEntry object
        """
        if not isinstance(entry, ConfigSchemaEntry):
            raise TypeError(f"Entry must be a ConfigSchemaEntry, got {type(entry)}")
        
        path_str = entry.get_path_str()
        self.entries[path_str] = entry
                
        debug(f"Added schema entry: {path_str}")
    
    def add_entries(self, entries):
        """
        Add multiple entries to the schema.
        
        Args:
            entries: A list of ConfigSchemaEntry objects or a dictionary mapping paths to entries
        """
        if isinstance(entries, dict):
            for key, entry in entries.items():
                if not isinstance(entry, ConfigSchemaEntry):
                    entry = ConfigSchemaEntry(path=key, **entry)
                self.add_entry(entry)
        elif isinstance(entries, list):
            for entry in entries:
                self.add_entry(entry)
        else:
            raise TypeError(f"Entries must be a list or dictionary, got {type(entries)}")
    
    def build_from_config(self, config):
        """
        Build a schema from a configuration dictionary.
        
        Args:
            config: A configuration dictionary to build the schema from
        """
        self._build_from_config_recursive(config)
    
    def _build_from_config_recursive(self, config, path=None):
        """
        Recursively build a schema from a configuration dictionary.
        
        Args:
            config: A configuration dictionary to build the schema from
            path: The current path in the configuration dictionary
        """
        if path is None:
            path = []
        
        if isinstance(config, dict):
            for key, value in config.items():
                new_path = path + [key]
                if isinstance(value, dict):
                    self._build_from_config_recursive(value, new_path)
                else:
                    entry = ConfigSchemaEntry(
                        path=new_path,
                        format=type(value),
                        default=value
                    )
                    self.add_entry(entry)
    
    def validate(self, config):
        """
        Validate a configuration dictionary against this schema.
        
        Args:
            config: The configuration dictionary to validate
            
        Returns:
            The validated configuration dictionary
            
        Raises:
            ValueError: If required entries are missing or values are invalid
        """
        # First pass: check for required entries and apply defaults
        for path_str, entry in self.entries.items():
            path = entry.path
            
            # Check if the entry exists in the configuration
            value = self._get_value_from_path(config, path)
            
            if value is None:
                if entry.required:
                    if entry.default is not None:
                        # Entry is required but missing, use default
                        self._set_value_at_path(config, path, entry.default)
                    else:
                        # Entry is required, has no default, and is missing
                        raise ValueError(f"Required configuration entry missing: {path_str}")
                elif entry.default is not None:
                    # Entry is not required but has a default
                    self._set_value_at_path(config, path, entry.default)
        
        # Second pass: validate values
        for path_str, entry in self.entries.items():
            path = entry.path
            value = self._get_value_from_path(config, path)
            
            # Skip validation if the value is None and the entry is nullable
            if value is None and entry.nullable:
                continue
            
            # Validate the value
            try:
                validated_value = entry.validate(value)
                if validated_value != value:
                    self._set_value_at_path(config, path, validated_value)
            except (ValueError, TypeError) as e:
                # Re-raise with a more descriptive message
                raise type(e)(f"Error validating {path_str}: {str(e)}")
        
        return config
    
    def _get_value_from_path(self, config, path):
        """
        Get a value from a configuration dictionary using a path.
        
        Args:
            config: The configuration dictionary
            path: The path as a list of keys
            
        Returns:
            The value at the path, or None if the path does not exist
        """
        current = config
        for key in path:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None
        return current
    
    def _set_value_at_path(self, config, path, value):
        """
        Set a value in a configuration dictionary using a path.
        
        Args:
            config: The configuration dictionary
            path: The path as a list of keys
            value: The value to set
        """
        current = config
        for key in path[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        current[path[-1]] = value