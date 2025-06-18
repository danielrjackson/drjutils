# DRJ Utils Documentation

This directory contains documentation for the DRJ Utils package.

## Overview

DRJ Utils is a collection of utilities designed to simplify common tasks in Python projects:

- **Configuration Management**: Load, validate, and save configuration files with schema validation
- **Logging**: Zero-configuration logging with contextual information
- **Common Utilities**: Path management, time formatting, and other shared functions

## Module Documentation

- [Configuration Utilities](config/README.md): Documentation for the configuration utilities
- [Logging Utilities](log/README.md): Documentation for the logging utilities
- [Common Utilities](common/README.md): Documentation for the common utilities
- [Developer Notes](notes/README.md): Internal notes on changes and lessons learned

## Installation

### As a Git Submodule

The recommended way to use DRJ Utils is as a git submodule:

```bash
# Add the submodule to a 'libs' directory in your project
git submodule add https://github.com/yourusername/drjutils.git libs/drjutils
```

### Usage

Once installed, you can import the utilities in your code:

```python
# Config utilities
from libs.drjutils.config import ConfigLoader, ConfigSchema, ConfigSchemaEntry

# Logging utilities
from libs.drjutils.log import debug, info, warning, error, critical

# Common utilities
from libs.drjutils.common.time import format_run_time
from libs.drjutils.common.paths import BaseProjectPaths
```

## Quick Start Examples

### Logging

```python
from libs.drjutils.log import info, debug, warning, error

# Basic logging - works without any configuration
info("Application started")

# Debug with location information (file, line number)
debug("Processing data", include_location=True)

# Warning and error messages
warning("Resource usage is high")
error("Failed to connect to database", include_traceback=True)
```

### Configuration

```python
from libs.drjutils.config import ConfigLoader, ConfigSchema, ConfigSchemaEntry

# Load configuration
config_loader = ConfigLoader("./config", "config.yaml")

# Access configuration values
database_url = config_loader.get("database.url")
app_name = config_loader.get("app.name", "Default App Name")

# Define a schema for validation
schema = ConfigSchema([
    ConfigSchemaEntry(path="database.url", format_type=str, required=True),
    ConfigSchemaEntry(path="app.name", format_type=str, default="Default App Name"),
    ConfigSchemaEntry(path="app.port", format_type=int, default=8080)
])

# Validate configuration
validated_config = schema.validate(config_loader.config)
```

### Common Utilities

```python
from libs.drjutils.common.paths import BaseProjectPaths
from libs.drjutils.common.time import format_run_time
from datetime import timedelta

# Path management
paths = BaseProjectPaths()
print(f"Project root: {paths.project_root}")
print(f"Config directory: {paths.config_dir}")

# Time formatting
duration = timedelta(hours=2, minutes=30, seconds=45)
formatted_time = format_run_time(duration)
print(f"Duration: {formatted_time}")  # Outputs: "2h 30m 45.000s"
```

## Contributing

Contributions to DRJ Utils are welcome! Please ensure that any contributions maintain the existing code style and include appropriate tests and documentation.

## License

Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)
