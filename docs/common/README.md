# Common Utilities

The DRJ Utils common module provides a collection of general-purpose utilities that are useful across different projects.

## Components

- **Path Management**: Discover project roots and manage directory structures
- **Time Formatting**: Format time deltas in a human-readable way

## Path Management

The `paths.py` module provides utilities for discovering project roots and managing directory structures.

### BaseProjectPaths

The `BaseProjectPaths` class discovers the project root and provides access to common project directories.

#### Basic Usage

```python
from libs.drjutils.common.paths import BaseProjectPaths

# Initialize with automatic project root discovery
paths = BaseProjectPaths()

# Access common directories
print(f"Project root: {paths.project_root}")
print(f"Config directory: {paths.config_dir}")
print(f"Logs directory: {paths.logs_dir}")

# Ensure directories exist
paths.ensure_dirs_exist()
```

#### Custom Project Root

```python
from libs.drjutils.common.paths import BaseProjectPaths
from pathlib import Path

# Specify a custom project root
custom_root = Path("/path/to/project")
paths = BaseProjectPaths(project_root=custom_root)
```

#### Extending for Project-Specific Paths

You can extend `BaseProjectPaths` for your specific project structure:

```python
from libs.drjutils.common.paths import BaseProjectPaths
from pathlib import Path

class MyProjectPaths(BaseProjectPaths):
    def __init__(self, project_root=None):
        super().__init__(project_root)
        
        # Add project-specific paths
        self.data_dir = self.project_root / "data"
        self.models_dir = self.project_root / "models"
        self.output_dir = self.project_root / "output"
    
    def ensure_dirs_exist(self):
        # Call parent method to ensure base directories exist
        super().ensure_dirs_exist()
        
        # Ensure project-specific directories exist
        for dir_path in [self.data_dir, self.models_dir, self.output_dir]:
            dir_path.mkdir(exist_ok=True)
```

#### Methods and Attributes

| Attribute/Method | Type | Description |
|------------------|------|-------------|
| `project_root` | Path | Root directory of the project |
| `config_dir` | Path | Directory for configuration files |
| `logs_dir` | Path | Directory for log files |
| `ensure_dirs_exist()` | method | Creates directories if they don't exist |
| `_discover_project_root()` | method | Discovers the project root based on common markers |

## Time Formatting

The `time.py` module provides utilities for formatting time values in a human-readable way.

### format_run_time

The `format_run_time` function formats a timedelta as a human-readable string with appropriate units.

#### Basic Usage

```python
from libs.drjutils.common.time import format_run_time
from datetime import timedelta

# Format a timedelta
duration = timedelta(days=1, hours=2, minutes=30, seconds=45.123)
formatted = format_run_time(duration)
print(formatted)  # Outputs: "1d 02h 30m 45.123s"

# Format a shorter duration
short_duration = timedelta(seconds=75.5)
formatted = format_run_time(short_duration)
print(formatted)  # Outputs: "01m 15.500s"
```

#### Using with time measurements

```python
import time
from datetime import datetime
from libs.drjutils.common.time import format_run_time

# Measure function execution time
start_time = datetime.now()

# Some operation that takes time
time.sleep(2.5)  # Simulating work

# Calculate and format duration
duration = datetime.now() - start_time
print(f"Operation completed in {format_run_time(duration)}")
```

#### Features

- Automatically scales units based on the duration
- Always shows seconds with millisecond precision
- Shows hours and minutes with leading zeros
- Omits larger units if they're zero
- Always shows at least seconds

## Examples

### Combining Path and Time Utilities

```python
from libs.drjutils.common.paths import BaseProjectPaths
from libs.drjutils.common.time import format_run_time
from datetime import datetime
import os

# Initialize paths
paths = BaseProjectPaths()
print(f"Project root: {paths.project_root}")

# Create a timestamped output directory
start_time = datetime.now()
timestamp = start_time.strftime("%Y%m%d_%H%M%S")
output_dir = paths.project_root / "output" / timestamp
os.makedirs(output_dir, exist_ok=True)

# Do some work...
import time
time.sleep(2.5)  # Simulating work

# Calculate duration
duration = datetime.now() - start_time
print(f"Operation completed in {format_run_time(duration)}")

# Save results
with open(output_dir / "results.txt", "w") as f:
    f.write(f"Operation completed in {format_run_time(duration)}\n")
    f.write(f"Results saved at {datetime.now().isoformat()}\n")
```

### Using with Logging

```python
from libs.drjutils.common.paths import BaseProjectPaths
from libs.drjutils.common.time import format_run_time
from libs.drjutils.log import info, debug
from datetime import datetime

# Initialize paths
paths = BaseProjectPaths()
info(f"Project root: {paths.project_root}")

# Measure operation time
start_time = datetime.now()
debug("Starting operation...")

# Do some work...
import time
time.sleep(1.5)  # Simulating work

# Log completion with formatted duration
duration = datetime.now() - start_time
info(f"Operation completed in {format_run_time(duration)}")
```

## Best Practices

1. **Use BaseProjectPaths for consistent path management**:
   ```python
   # Create a project-specific paths class in a central location
   from libs.drjutils.common.paths import BaseProjectPaths
   
   class MyAppPaths(BaseProjectPaths):
       def __init__(self):
           super().__init__()
           self.data_dir = self.project_root / "data"
           # Add other project-specific paths
   
   # Then use it consistently throughout your application
   paths = MyAppPaths()
   ```

2. **Use format_run_time for all duration formatting**:
   ```python
   # Instead of formatting manually
   # Don't do this:
   # print(f"Completed in {duration.total_seconds():.2f} seconds")
   
   # Do this:
   print(f"Completed in {format_run_time(duration)}")
   ```

3. **Create a context manager for timing operations**:
   ```python
   from contextlib import contextmanager
   from datetime import datetime
   from libs.drjutils.common.time import format_run_time
   from libs.drjutils.log import info
   
   @contextmanager
   def timed_operation(description):
       start_time = datetime.now()
       info(f"Starting: {description}")
       try:
           yield
       finally:
           duration = datetime.now() - start_time
           info(f"Completed: {description} in {format_run_time(duration)}")
   
   # Usage
   with timed_operation("Database backup"):
       # Operations to time...
       pass
   ```
