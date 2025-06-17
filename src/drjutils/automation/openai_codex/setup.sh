#!/bin/bash

# This script sets up the environment for OpenAI Codex automation.
# It assumes that pyenv is already installed and configured.
# It also assumes that the current directory is the root of the drjutils package.
# It installs Python 3.13, sets it as the active version, and installs necessary packages.
# Exit immediately if a command exits with a non-zero status

# This script is intended to be copied into the Setup script box on the environment setup page
# of the OpenAI Codex automation tool.

set -e

# Ensure Python 3.13 is active (adjust version if needed)
pyenv shell 3.13.3

sudo apt-get update
sudo apt-get install -y python3-venv

python3 -m pip install --upgrade pip
python3 -m pip install hatchling editables

# Install package with development dependencies
pip install -e .[dev] --no-build-isolation