# API Key Management

The DRJ Utils package includes a secure API key management system that integrates with system credential stores.

## Overview

The API key management system allows you to:

1. **Define API keys** in a YAML configuration file
2. **Retrieve API keys** from secure credential stores (like Windows Credential Manager)
3. **Store API keys** securely without hardcoding them in your code
4. **Share key configurations** across multiple projects

This approach improves security by storing sensitive API keys in the system's credential manager rather than in plaintext configuration files.

## Configuration Format

API keys are defined in an `api_keys.yaml` file using this format:

```yaml
# API Keys
# Stored in Windows Credential Manager
keys:
  - name: OpenAI_DevKey
    url: OpenAI_API
    username: My_Dev_Key

  - name: AnthropicClaude
    url: Anthropic_API
    username: Claude_Key
```

Each key entry requires three fields:
- `name`: A unique identifier for the key in your application
- `url`: The service name in the credential store
- `username`: The account identifier in the credential store

## Configuration Location

The system searches for an `api_keys.yaml` file in these locations (in order):

1. **Project-specific**: In your project directory or any parent directory
2. **User-specific**: In `~/.drjutils/api_keys.yaml` 
3. **Package template**: The template included in the DRJ Utils package

This allows you to:
- Override configurations on a per-project basis
- Share configurations across all your projects
- Have sensible defaults from the package template

## Basic Usage

### Retrieving an API Key

```python
from libs.drjutils.config.api_keys import get_api_key

# Get an API key by name
openai_key = get_api_key("OpenAI_DevKey")

# Use the key in your application
if openai_key:
    # Example with OpenAI
    import openai
    openai.api_key = openai_key
    
    # Make API calls...
else:
    print("API key not found or not accessible")
```

### Working with Multiple Keys

```python
from libs.drjutils.config.api_keys import get_key_manager

# Initialize the key manager
key_manager = get_key_manager()

# List all configured keys
for key in key_manager.get_all_keys():
    print(f"Found key: {key}")

# Get specific keys
openai_key = key_manager.get_key("OpenAI_DevKey")
anthropic_key = key_manager.get_key("AnthropicClaude")
```

### Setting API Keys

```python
from libs.drjutils.config.api_keys import get_key_manager

key_manager = get_key_manager()

# Get a key configuration
openai_config = key_manager.get_key_config("OpenAI_DevKey")

# Set the API key value in the credential store
if openai_config:
    success = openai_config.set_value("sk-your-actual-api-key")
    if success:
        print("API key stored successfully")
    else:
        print("Failed to store API key")
```

## Advanced Usage

### Custom Configuration Path

```python
from libs.drjutils.config.api_keys import get_key_manager

# Specify a custom path for the api_keys.yaml file
custom_path = "/path/to/your/api_keys.yaml"
key_manager = get_key_manager(custom_path)

# Use the key manager as normal
api_key = key_manager.get_key("CustomAPI")
```

### Creating a Central Configuration

To share configurations across all your projects:

1. Create a directory in your home folder:
   ```bash
   mkdir -p ~/.drjutils
   ```

2. Create or copy an api_keys.yaml file:
   ```bash
   cp /path/to/template/api_keys.yaml ~/.drjutils/
   ```

3. Edit the file to include your API key configurations:
   ```yaml
   # API Keys
   # Stored in Windows Credential Manager
   keys:
     - name: OpenAI_DevKey
       url: OpenAI_API
       username: My_Dev_Key
     
     - name: AnthropicClaude
       url: Anthropic_API
       username: Claude_Key
   ```

Now all your projects using DRJ Utils will have access to these key configurations.

### Direct Access to ApiKey Objects

```python
from libs.drjutils.config.api_keys import get_key_manager

key_manager = get_key_manager()

# Get the API key configuration object
openai_key_config = key_manager.get_key_config("OpenAI_DevKey")

if openai_key_config:
    print(f"Service: {openai_key_config.url}")
    print(f"Username: {openai_key_config.username}")
    
    # Get the key value
    key_value = openai_key_config.get_value()
    
    # Set a new key value
    openai_key_config.set_value("new-api-key-value")
```

## Windows Credential Manager Integration

The system uses the `keyring` package to interact with credential managers:

1. On Windows, this will use Windows Credential Manager
2. On macOS, this will use Keychain
3. On Linux, this will use secretservice or appropriate alternatives

### Viewing Stored Credentials in Windows

1. Open Control Panel
2. Go to User Accounts → Credential Manager
3. Switch to the "Windows Credentials" tab
4. Look for entries matching your `url` values (e.g., "OpenAI_API")

### Manually Adding Credentials

You can add credentials directly in Windows Credential Manager:

1. In Credential Manager, click "Add a Windows credential"
2. For "Internet or network address", enter the `url` from your config (e.g., "OpenAI_API")
3. For "User name", enter the `username` from your config
4. For "Password", enter your actual API key
5. Click "OK" to save

## Interactive Key Management

This example shows how to create an interactive key management tool:

```python
from libs.drjutils.config.api_keys import get_key_manager, get_api_key
from libs.drjutils.log import info, error

def manage_api_keys():
    key_manager = get_key_manager()
    keys = key_manager.get_all_keys()
    
    print("API Key Management")
    print("==================")
    print(f"Found {len(keys)} configured keys:")
    
    for i, key in enumerate(keys):
        # Check if the key exists in the credential store
        value = key.get_value()
        status = "✓" if value else "✗"
        print(f"{i+1}. {key.name} [{status}]")
    
    print("\nOptions:")
    print("1. View a key")
    print("2. Set a key")
    print("3. Exit")
    
    choice = input("Enter your choice: ")
    
    if choice == "1":
        key_name = input("Enter key name: ")
        key_config = key_manager.get_key_config(key_name)
        if key_config:
            value = key_config.get_value()
            if value:
                print(f"Key: {value[:4]}...{value[-4:] if len(value) > 8 else ''}")
            else:
                print("Key not found in credential store")
        else:
            print(f"No configuration found for {key_name}")
    
    elif choice == "2":
        key_name = input("Enter key name: ")
        key_config = key_manager.get_key_config(key_name)
        if key_config:
            value = input("Enter key value: ")
            if key_config.set_value(value):
                print("Key stored successfully")
            else:
                print("Failed to store key")
        else:
            print(f"No configuration found for {key_name}")

if __name__ == "__main__":
    manage_api_keys()
```

## Best Practices

1. **Never hardcode API keys** in your source code
2. **Use descriptive names** in your `api_keys.yaml` file
3. **Keep service names consistent** across projects (e.g., always use "OpenAI_API")
4. **Avoid storing keys in version control** (add api_keys.yaml to .gitignore)
5. **Use different usernames** for development vs. production keys
6. **Regularly rotate API keys** for security
7. **Create a central configuration** in `~/.drjutils/api_keys.yaml` for convenience
