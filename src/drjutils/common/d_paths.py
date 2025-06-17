"""
Path Management Utilities

This module provides path management utilities for discovering project roots
and managing common directory structures.

Classes:
    BaseProjectPaths: Base class for project paths

Copyright 2025 Daniel Robert Jackson
"""

import os
from pathlib import Path

__all__ = ["BaseProjectPaths"]

class BaseProjectPaths:
    """
    Base class for project paths.
    
    Provides common path discovery and management functionality.
    
    Attributes:
        project_root: Root directory of the project
        config_dir: Directory for configuration files
        logs_dir: Directory for log files
    """
    
    def __init__(self, project_root=None):
        """
        Initialize the project paths.
        
        Args:
            project_root (str or Path, optional): Path to the project root directory.
                If None, will attempt to discover the project root.
        """
        # Determine project root
        self.project_root = self._discover_project_root() if project_root is None else Path(project_root)
        
        # Common directories
        self.config_dir = self.project_root / "config"
        self.logs_dir = self.project_root / "logs"
        
    def _discover_project_root(self):
        """
        Attempt to discover the project root directory.
        
        Looks for common project indicators like src/, config/, .git/, etc.
        
        Returns:
            Path: The discovered project root directory
        """
        # Start with the current working directory
        current_path = Path.cwd().resolve()
        
        # Look for common project indicators
        while current_path != current_path.parent:
            # Check for common project indicators
            if any((current_path / indicator).exists() for indicator in ["src", "config", ".git"]):
                return current_path
            
            # Move up one directory
            current_path = current_path.parent
        
        # If no indicators found, use current directory
        return Path.cwd().resolve()
    
    def ensure_dirs_exist(self):
        """
        Ensure that common directories exist.
        
        Creates directories if they do not exist.
        """
        for dir_path in [self.config_dir, self.logs_dir]:
            os.makedirs(dir_path, exist_ok=True)
    
    def __str__(self):
        """String representation of the project paths."""
        return f"ProjectPaths(root='{self.project_root}')"
