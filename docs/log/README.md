# Logging Utilities

The DRJ Utils logging module provides a zero-configuration logging system with contextual information. It's designed to work immediately without any setup while offering advanced capabilities when needed.

## Features

- **Zero-configuration**: Works immediately upon import without any setup
- **Automatic path detection**: Discovers project structure to set up log directories
- **Contextual information**: Optionally includes file name, line number, and function name
- **Multiple outputs**: Logs to both console and file by default
- **Stack traces**: Automatically includes stack traces for errors when appropriate
- **YAML configuration**: Can be configured from YAML files

## Basic Usage

```python
from libs.drjutils.log import debug, info, warning, error, critical, exception

# Basic logging - works without any configuration
info("Application started")

# Debug message with location information (file, line number)
debug("Processing data", include_location=True)

# Warning message
warning("Resource usage is high")

# Error message with stack trace
error("Failed to connect to database", include_traceback=True)

# Critical error
critical("System failure detected")

# Exception with automatic traceback (use in except blocks)
try:
    result = 10 / 0
except Exception as e:
    exception(f"Calculation failed: {e}")
```

## Logging Functions

| Function | Default Level | Location Included | Description |
|----------|--------------|------------------|-------------|
| `debug()` | DEBUG | Yes | Detailed information for debugging |
| `info()` | INFO | No | Normal operational messages |
| `warning()` | WARNING | Yes | Warning messages |
| `error()` | ERROR | Yes | Error messages |
| `critical()` | CRITICAL | Yes | Critical failures |
| `exception()` | ERROR | Yes | Error with exception traceback |

### Function Parameters

Each logging function accepts these parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| `msg` | str | The message to log |
| `include_location` | bool | Whether to include file/line/function info |
| `include_traceback` | bool | Whether to include a stack trace (error/critical only) |

## Configuration

The logging system auto-configures itself on first use, but you can explicitly configure it for more control.

### Explicit Configuration

```python
from libs.drjutils.log import configure, debug, info
import logging

# Configure logging with custom settings
log_dir = configure(
    log_dir="./custom_logs",         # Custom log directory
    console_level=logging.DEBUG,     # Show debug messages in console
    file_level=logging.INFO,         # Only INFO and above in log files
    log_format="%(asctime)s - %(levelname)s - %(message)s"  # Custom format
)

info(f"Logging configured. Log directory: {log_dir}")
```

### Configuration from YAML

```python
from libs.drjutils.log import load_config_from_yaml, info

# Load logging configuration from a YAML file
load_config_from_yaml("./config/logging.yaml")

info("Logging configured from YAML")
```

Example YAML configuration:

```yaml
logging:
  dir: "logs"
  console_level: "DEBUG"
  file_level: "INFO"
  format: "%(levelname)s - %(asctime)s - %(message)s"
```

## Advanced Usage

### Controlling Location Information

You can control whether location information is included in each log message:

```python
# Default behavior for info (no location)
info("Normal operation message")

# Include location for specific info messages
info("Important configuration loaded", include_location=True)

# Disable location for debug (normally included)
debug("Verbose message", include_location=False)
```

### Including Stack Traces

For error and critical messages, you can include stack traces:

```python
# Error with stack trace
error("Database connection failed", include_traceback=True)

# Critical error with stack trace (default behavior)
critical("System failure detected")  # Stack trace included by default

# Critical error without stack trace
critical("Minor system issue", include_traceback=False)
```

### Usage in Classes

The logging functions can be used directly in any file or class:

```python
from libs.drjutils.log import info, debug, error

class DatabaseConnector:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        info(f"Initializing database connector")
        
    def connect(self):
        try:
            debug(f"Connecting to database", include_location=True)
            # Connection code here...
            info(f"Connected to database successfully")
            return True
        except Exception as e:
            error(f"Failed to connect to database: {e}", include_traceback=True)
            return False
```

## Log File Structure

By default, logs are stored in timestamped directories within the project's `logs` directory:

```
project_root/
└── logs/
    └── 2025-01-15_10-30/
        └── app.log
```

This structure ensures that:
- Log files are organized by run timestamp
- You can easily find logs from specific application runs
- Old logs remain accessible but separated from new runs

## Under the Hood

The logging system:

1. **Auto-discovers project structure** to find appropriate log locations
2. **Creates necessary directories** for log files
3. **Sets up console and file handlers** for Python's built-in logging system
4. **Configures appropriate formatting** for log messages
5. **Provides context information** by inspecting the call stack

## Best Practices

1. **Use appropriate log levels**:
   - `debug`: For detailed troubleshooting information
   - `info`: For general operational information
   - `warning`: For potential issues that don't prevent operation
   - `error`: For failures that affect functionality
   - `critical`: For severe failures that prevent operation

2. **Include context in messages**:
   ```python
   # Good
   info(f"User {user_id} logged in successfully")
   
   # Not as helpful
   info("Login successful")
   ```

3. **Use structured logging for complex data**:
   ```python
   # For complex structures, consider JSON-style representation
   debug(f"Request data: {json.dumps(request_data, indent=2)}")
   ```

4. **Configure early in application startup**:
   ```python
   # In your application's main entry point
   from libs.drjutils.log import configure
   
   def main():
       configure(log_dir="./logs")
       # Rest of application...
   ```

5. **Include location for important informational messages**:
   ```python
   info("Application starting with configuration", include_location=True)
   ```
