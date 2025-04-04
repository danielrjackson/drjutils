# DRJ Utils

A collection of utility modules for Python projects.

## Overview

This repository contains utilities for:

- **Configuration Management**: Loading, validating, and saving configuration files
- **Logging**: Simple, zero-configuration logging
- **Common Utilities**: Path management, time formatting, and other shared functions

## Installation

### As a Git Submodule

Add this repository as a submodule to your project:

```bash
# Add the submodule to a 'libs' directory in your project
git submodule add https://github.com/danielrjackson/drjutils.git libs/drjutils
```

### Usage

Import the utilities in your code:

```python
# Config utilities
from libs.drjutils.config import ConfigLoader, ConfigSchema

# Logging utilities
from libs.drjutils.log import debug, info, warning, error, critical

# Common utilities
from libs.drjutils.common.time import format_run_time
from libs.drjutils.common.paths import BaseProjectPaths
```

## Components

### Configuration Utilities

- `ConfigLoader`: Load and save configuration from YAML files
- `ConfigSchema`: Validate configuration structure and values
- `ConfigSchemaEntry`: Define and validate individual configuration entries

### Logging Utilities

Zero-configuration logging with contextual information:

```python
from libs.drjutils.log import info, debug

info("Application started")
debug("Processing data", include_location=True)  # Shows file and line number
```

### Common Utilities

- **Path Management**: Discover project roots, manage common directory structures
- **Time Formatting**: Format time deltas and timestamps

---

*Copyright © 2025 Daniel Jackson. Licensed under [CC BY-NC-ND 4.0].*

![LicenseImage]

*Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International* [Official CC License]

[//]: # (Links)
[CC BY-NC-ND 4.0]:          LICENSE
[LicenseImage]:             docs/images/license.png
[Official CC License]:      https://creativecommons.org/licenses/by-nc-nd/4.0/