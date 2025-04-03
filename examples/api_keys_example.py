"""
Example of using the API key management utilities.

This shows how to:
1. Load API key configurations from an api_keys.yaml file
2. Retrieve API keys from Windows Credential Manager
3. Store API keys in Windows Credential Manager
4. Use the keys in your application

Copyright 2025 Daniel Robert Jackson
"""

from pathlib import Path
import os

# Import from the drjutils library
from libs.drjutils.config.api_keys import get_key_manager, get_api_key
from libs.drjutils.log import info, warning, error, configure

def main():
    # Configure logging
    configure()
    info("API Key Management Example")
    
    # Initialize the key manager - it will automatically find a configuration
    key_manager = get_key_manager()
    
    # List all configured API keys
    keys = key_manager.get_all_keys()
    info(f"Found {len(keys)} API key configurations:")
    for key in keys:
        info(f"  - {key}")
    
    # Get a specific API key
    openai_key = get_api_key("OpenAI_DevKey")
    
    if openai_key:
        # The key is available - we can use it
        info("OpenAI API key retrieved successfully")
        
        # Only show a few characters for security
        masked_key = mask_api_key(openai_key)
        info(f"Key value (masked): {masked_key}")
        
        # Example of using the key for API calls
        info("Example API call using the key (simulated):")
        simulate_openai_api_call(openai_key)
    else:
        warning("OpenAI API key not found or could not be retrieved")
        # Offer to set the key
        store_key_interactively("OpenAI_DevKey")

def mask_api_key(key: str) -> str:
    """
    Mask an API key for display, showing only the first and last few characters.
    
    Args:
        key: The API key to mask
        
    Returns:
        The masked API key
    """
    if not key or len(key) < 8:
        return "***"
    
    return key[:4] + "..." + key[-4:]

def store_key_interactively(key_name: str) -> bool:
    """
    Prompt the user to input an API key and store it.
    
    Args:
        key_name: Name of the API key to store
        
    Returns:
        True if the key was stored successfully, False otherwise
    """
    info(f"Would you like to store your {key_name} now? (y/n)")
    response = input().strip().lower()
    
    if response == 'y' or response == 'yes':
        # Get the key configuration
        key_manager = get_key_manager()
        key_config = key_manager.get_key_config(key_name)
        
        if key_config:
            # Prompt for the key value
            print(f"Enter your {key_name} value: ", end='')
            key_value = input().strip()
            
            # Store the key
            if key_config.set_value(key_value):
                info(f"{key_name} stored successfully")
                return True
            else:
                error(f"Failed to store {key_name}")
        else:
            error(f"No configuration found for {key_name}")
    
    return False

def simulate_openai_api_call(api_key: str) -> None:
    """
    Simulate an OpenAI API call using the API key.
    
    Args:
        api_key: The OpenAI API key
    """
    info("Connecting to OpenAI API...")
    info("Sending request with API key in headers...")
    info("Received response from OpenAI API")
    
    # Example code for a real OpenAI API call:
    """
    import openai
    
    # Configure the client with your API key
    openai.api_key = api_key
    
    # Make an API request
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, world!"}
        ]
    )
    
    # Process the response
    assistant_response = completion.choices[0].message.content
    info(f"OpenAI response: {assistant_response}")
    """

if __name__ == "__main__":
    main()
