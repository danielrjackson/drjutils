# Configuration Utilities

The DRJ Utils configuration module provides tools for loading, validating, and saving configuration files with schema validation.

## Components

- **ConfigLoader**: Load and save configuration from YAML files
- **ConfigSchema**: Validate configuration structure and values
- **ConfigSchemaEntry**: Define and validate individual configuration entries
- **Utility Functions**: Merge configs, find config files, and more

## ConfigLoader

The `ConfigLoader` class provides methods for loading configuration from YAML files and accessing values.

### Basic Usage

```python
from libs.drjutils.config import ConfigLoader

# Initialize with a configuration file path
config_loader = ConfigLoader("./config/config.yaml")

# Access configuration values
database_url = config_loader.get("database.url")
app_port = config_loader.get("app.port", 8080)  # Default value if not found

# Modify configuration
config_loader.set("app.version", "1.0.1")

# Save configuration
config_loader.save_config()
```

### Advanced Usage

```python
# Initialize with a directory and specific file
config_loader = ConfigLoader(
    config_path="./config", 
    config_file="production.yaml"
)

# Initialize with schema validation
from libs.drjutils.config import ConfigSchema

schema = ConfigSchema(...)
config_loader = ConfigLoader(
    config_path="./config/config.yaml",
    validate_schema=True,
    schema=schema
)

# Save to a different file
config_loader.save_config(output_path="./config/modified_config.yaml")
```

### Constructor Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `config_path` | str | Path to the configuration file or directory |
| `config_file` | str, optional | Filename (required if config_path is a directory) |
| `validate_schema` | bool, optional | Whether to validate the config against a schema |
| `schema` | ConfigSchema, optional | Schema to validate against |

### Methods

| Method | Description |
|--------|-------------|
| `get(key_path, default=None)` | Get a value by dot-notation path |
| `set(key_path, value)` | Set a value by dot-notation path |
| `save_config(config=None, output_path=None)` | Save configuration to a file |

## ConfigSchema

The `ConfigSchema` class validates configuration dictionaries against a set of schema entries.

### Basic Usage

```python
from libs.drjutils.config import ConfigSchema, ConfigSchemaEntry

# Define schema with entries
schema = ConfigSchema([
    ConfigSchemaEntry(path="app.name", format_type=str, required=True),
    ConfigSchemaEntry(path="app.port", format_type=int, default=8080),
    ConfigSchemaEntry(path="logging.level", format_type=str, 
                     default="INFO", validator=lambda x: x in ["DEBUG", "INFO", "WARNING", "ERROR"])
])

# Validate a configuration dictionary
validated_config = schema.validate(config_dict)
```

### Building From Existing Config

```python
# Automatically build a schema from an existing configuration
existing_config = {
    "app": {
        "name": "My App",
        "port": 8080
    },
    "database": {
        "url": "postgres://localhost/mydb"
    }
}

schema = ConfigSchema(source_config=existing_config)

# Add custom validators later
schema.entries["app.port"].validator = (1024, 65535)  # Range validator for port
```

### Methods

| Method | Description |
|--------|-------------|
| `add_entry(entry)` | Add a schema entry |
| `add_entries(entries)` | Add multiple schema entries |
| `build_from_config(config)` | Build schema from a configuration dictionary |
| `validate(config)` | Validate a configuration dictionary |

## ConfigSchemaEntry

The `ConfigSchemaEntry` class defines validation rules for a single configuration entry.

### Basic Usage

```python
from libs.drjutils.config import ConfigSchemaEntry
import re

# Path-based entry
db_url = ConfigSchemaEntry(
    path="database.url",  # Can be a string or list ["database", "url"]
    format_type=str,
    required=True
)

# With default value
port = ConfigSchemaEntry(
    name="port",
    path=["app", "port"],
    format_type=int,
    default=8080,
    validator=(1024, 65535)  # Range for port numbers
)

# With regex validator
email = ConfigSchemaEntry(
    path="user.email",
    format_type=str,
    validator=re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
)

# With custom validator function
log_level = ConfigSchemaEntry(
    path="logging.level",
    format_type=str,
    default="INFO",
    validator=lambda x: x in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
)
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | str, optional | Name of the entry (last path key) |
| `path` | str or List[str] | Path to the entry (dot notation or list) |
| `format_type` | type | Data type (str, int, float, bool, Path, etc.) |
| `default` | Any, optional | Default value if not present |
| `validator` | callable/tuple/regex | Validator for the entry |
| `nullable` | bool | Whether None is allowed (default: True) |
| `required` | bool | Whether the entry is required (default: True) |

### Validator Types

- **Range (for numbers)**: Tuple of (min, max)
- **Regex (for strings)**: re.Pattern object or regex string
- **Function**: A callable that returns True/False or a modified value

## Utility Functions

The `utils.py` module provides additional utility functions for working with configurations.

### merge_configs

Merges two configuration dictionaries recursively.

```python
from libs.drjutils.config.utils import merge_configs

base_config = {"app": {"name": "Base App", "port": 8080}}
override_config = {"app": {"port": 9000}}

merged = merge_configs(base_config, override_config)
# Result: {"app": {"name": "Base App", "port": 9000}}
```

### find_config_file

Searches for a configuration file in common locations.

```python
from libs.drjutils.config.utils import find_config_file

# Find a config file in default locations
config_path = find_config_file("app_config.yaml")

# Search in additional locations
config_path = find_config_file(
    "app_config.yaml", 
    search_paths=["/etc/myapp", "/usr/local/etc/myapp"]
)
```

### generate_sample_config

Generates a sample configuration from a schema.

```python
from libs.drjutils.config.utils import generate_sample_config

# Generate a sample configuration based on a schema
sample_config = generate_sample_config(schema)
```

## Complete Example

```python
from libs.drjutils.config import ConfigLoader, ConfigSchema, ConfigSchemaEntry
import re

# Define schema
schema = ConfigSchema([
    ConfigSchemaEntry(path="app.name", format_type=str, default="My Application"),
    ConfigSchemaEntry(path="app.port", format_type=int, default=8080, validator=(1024, 65535)),
    ConfigSchemaEntry(path="database.url", format_type=str, required=True),
    ConfigSchemaEntry(path="logging.level", format_type=str, default="INFO",
                     validator=lambda x: x.upper() if x.upper() in ["DEBUG", "INFO", "WARNING", "ERROR"] else "INFO"),
    ConfigSchemaEntry(path="email.admin", format_type=str, nullable=True,
                     validator=re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"))
])

try:
    # Load and validate configuration
    config_loader = ConfigLoader("./config/config.yaml", validate_schema=True, schema=schema)
    
    # Access validated configuration
    app_name = config_loader.get("app.name")
    db_url = config_loader.get("database.url")
    
    # Modify and save
    config_loader.set("app.version", "1.0.1")
    config_loader.save_config()
    
except (FileNotFoundError, ValueError) as e:
    print(f"Configuration error: {e}")
```

## Best Practices

1. **Define schemas explicitly** for better validation and documentation
2. **Include default values** for non-critical configuration
3. **Use validators** to ensure data integrity
4. **Use dot notation** for accessing nested configuration values
5. **Handle configuration errors** gracefully with try/except blocks
