# drjutils/log/logger.py

import os
import sys
import logging
import inspect
import traceback
from datetime import datetime
from pathlib import Path

# Global flag to track if logger has been configured
_CONFIGURED = False

# Default log directory - will be detected dynamically
_DEFAULT_LOG_DIR = None

def _get_project_root():
    """Determine the project root directory."""
    # Start with the directory containing this file
    current_path = Path(__file__).resolve()
    
    # Go up until we find the project root (where we expect to find directories like 'logs')
    # We'll look for src, config, or .git as indicators of the project root
    parent = current_path.parent
    while parent != parent.parent:  # Stop at filesystem root
        if (parent / "src").exists() or (parent / "config").exists() or (parent / ".git").exists():
            return parent
        parent = parent.parent
    
    # If we can't determine the project root, use the current working directory
    return Path.cwd().resolve()

def _ensure_log_dir():
    """Initialize the default log directory."""
    global _DEFAULT_LOG_DIR
    
    if _DEFAULT_LOG_DIR is None:
        project_root = _get_project_root()
        _DEFAULT_LOG_DIR = project_root / "logs"
    
    # Ensure the directory exists
    os.makedirs(_DEFAULT_LOG_DIR, exist_ok=True)
    
    return _DEFAULT_LOG_DIR

def _get_caller_info():
    """Get information about the calling file and line number."""
    # Get the current call stack
    stack = inspect.stack()
    
    # Find the first frame that isn't in this file or logging
    caller_frame = None
    for frame in stack[1:]:  # Skip this function's frame
        if frame.filename != __file__ and not frame.filename.endswith('logging/__init__.py'):
            caller_frame = frame
            break
    
    if not caller_frame:
        return "unknown", 0, "unknown"
    
    # Get the filename (try to make it relative to project root)
    try:
        project_root = _get_project_root()
        filename = Path(caller_frame.filename)
        try:
            rel_path = filename.relative_to(project_root)
            caller_file = str(rel_path)
        except ValueError:
            # If file is not within project root, use the basename
            caller_file = filename.name
    except Exception:
        # If anything goes wrong, just use the basename
        caller_file = Path(caller_frame.filename).name
    
    # Get line number and function name
    line_num = caller_frame.lineno
    func_name = caller_frame.function
    
    return caller_file, line_num, func_name

def _auto_configure():
    """Automatically configure logging if not already done."""
    global _CONFIGURED
    
    if _CONFIGURED:
        return
    
    # Create default log directory
    log_dir = _ensure_log_dir()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    log_dir = log_dir / timestamp
    os.makedirs(log_dir, exist_ok=True)
    
    # Configure root logger
    root_logger = logging.getLogger()
    
    # Remove any existing handlers to avoid duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Set overall level to DEBUG
    root_logger.setLevel(logging.DEBUG)
    
    # Create console handler with a higher log level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Create file handler for all logs
    log_file = log_dir / "app.log"
    file_handler = logging.FileHandler(str(log_file))
    file_handler.setLevel(logging.DEBUG)
    
    # Create formatters
    console_format = "%(levelname).1s|%(asctime)s|%(message)s"
    file_format = "%(levelname).1s|%(asctime)s|%(message)s"
    
    console_formatter = logging.Formatter(console_format)
    file_formatter = logging.Formatter(file_format)
    
    # Add formatters to handlers
    console_handler.setFormatter(console_formatter)
    file_handler.setFormatter(file_formatter)
    
    # Add handlers to root logger
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    # Mark as configured
    _CONFIGURED = True
    
    # Log that initialization is complete
    info(f"Logging initialized. Log file: {log_file}")

def configure(log_dir=None, console_level=logging.INFO, file_level=logging.DEBUG, log_format=None):
    """
    Explicitly configure logging system. This is optional - logging will
    auto-configure on first use if this isn't called.
    
    Args:
        log_dir (str or Path, optional): Directory for log files. If None, uses default.
        console_level (int): Logging level for console output.
        file_level (int): Logging level for file output.
        log_format (str, optional): Custom log format string.
    
    Returns:
        Path: The full path to the log directory.
    """
    global _CONFIGURED, _DEFAULT_LOG_DIR
    
    # Update default log directory if specified
    if log_dir:
        _DEFAULT_LOG_DIR = Path(log_dir)
    else:
        _ensure_log_dir()
    
    # Skip if already configured - allow reconfiguration in the future if needed
    if _CONFIGURED:
        return _DEFAULT_LOG_DIR
    
    # Create log directory
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    full_log_dir = _DEFAULT_LOG_DIR / timestamp
    os.makedirs(full_log_dir, exist_ok=True)
    
    # Configure root logger
    root_logger = logging.getLogger()
    
    # Remove any existing handlers to avoid duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Set overall level to the lower of the two levels
    root_logger.setLevel(min(console_level, file_level))
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    
    # Create file handler
    log_file = full_log_dir / "app.log"
    file_handler = logging.FileHandler(str(log_file))
    file_handler.setLevel(file_level)
    
    # Create formatters
    if log_format is None:
        console_format = "%(levelname).1s|%(asctime)s|%(message)s"
        file_format = "%(levelname).1s|%(asctime)s|%(message)s"
    else:
        console_format = log_format
        file_format = log_format
    
    console_formatter = logging.Formatter(console_format)
    file_formatter = logging.Formatter(file_format)
    
    # Add formatters to handlers
    console_handler.setFormatter(console_formatter)
    file_handler.setFormatter(file_formatter)
    
    # Add handlers to root logger
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    # Mark as configured
    _CONFIGURED = True
    
    # Log that initialization is complete using direct logging rather than our functions
    # to avoid circular calls during configuration
    logging.info(f"Logging explicitly configured. Log file: {log_file}")
    
    return full_log_dir

def load_config_from_yaml(config_path):
    """
    Load logging configuration from a YAML file.
    
    Args:
        config_path (str or Path): Path to the YAML configuration file.
    """
    try:
        import yaml
        
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            
        # Extract logging configuration
        log_config = config.get('logging', {})
        
        log_dir = log_config.get('dir')
        console_level = getattr(logging, log_config.get('console_level', 'INFO'))
        file_level = getattr(logging, log_config.get('file_level', 'DEBUG'))
        log_format = log_config.get('format')
        
        # Configure using extracted settings
        configure(log_dir, console_level, file_level, log_format)
        
        return True
        
    except (ImportError, FileNotFoundError, KeyError, AttributeError) as e:
        # If there's an error, log it but continue with default configuration
        if not _CONFIGURED:
            _auto_configure()
        error(f"Failed to load logging configuration from {config_path}: {e}")
        return False

def _format_message(msg, include_location=True):
    """Format message with caller location information if requested."""
    if not include_location:
        return msg
        
    file_name, line_num, func_name = _get_caller_info()
    return f"[{file_name}:{line_num} in {func_name}] {msg}"

def debug(msg, include_location=True):
    """
    Log a debug message.
    
    Args:
        msg (str): Message to log
        include_location (bool): Whether to include file/line/function info
    """
    if not _CONFIGURED:
        _auto_configure()
    logging.debug(_format_message(msg, include_location))

def info(msg, include_location=False):
    """
    Log an info message.
    
    Args:
        msg (str): Message to log
        include_location (bool): Whether to include file/line/function info
    """
    if not _CONFIGURED:
        _auto_configure()
    logging.info(_format_message(msg, include_location))

def warning(msg, include_location=True):
    """
    Log a warning message.
    
    Args:
        msg (str): Message to log
        include_location (bool): Whether to include file/line/function info
    """
    if not _CONFIGURED:
        _auto_configure()
    logging.warning(_format_message(msg, include_location))

def error(msg, include_location=True, include_traceback=False):
    """
    Log an error message.
    
    Args:
        msg (str): Message to log
        include_location (bool): Whether to include file/line/function info
        include_traceback (bool): Whether to include full traceback
    """
    if not _CONFIGURED:
        _auto_configure()
    
    formatted_msg = _format_message(msg, include_location)
    
    if include_traceback:
        # Get the exception info if there's an active exception
        exc_info = sys.exc_info()
        if exc_info[0] is not None:
            # There's an active exception, log with exc_info
            logging.error(formatted_msg, exc_info=exc_info)
            return
        
        # No active exception, append the traceback manually
        stack_trace = ''.join(traceback.format_stack()[:-1])  # Skip the current frame
        formatted_msg = f"{formatted_msg}\nStack trace:\n{stack_trace}"
    
    logging.error(formatted_msg)

def critical(msg, include_location=True, include_traceback=True):
    """
    Log a critical message.
    
    Args:
        msg (str): Message to log
        include_location (bool): Whether to include file/line/function info
        include_traceback (bool): Whether to include full traceback
    """
    if not _CONFIGURED:
        _auto_configure()
    
    formatted_msg = _format_message(msg, include_location)
    
    if include_traceback:
        # Get the exception info if there's an active exception
        exc_info = sys.exc_info()
        if exc_info[0] is not None:
            # There's an active exception, log with exc_info
            logging.critical(formatted_msg, exc_info=exc_info)
            return
        
        # No active exception, append the traceback manually
        stack_trace = ''.join(traceback.format_stack()[:-1])  # Skip the current frame
        formatted_msg = f"{formatted_msg}\nStack trace:\n{stack_trace}"
    
    logging.critical(formatted_msg)

def exception(msg, include_location=True):
    """
    Log an exception message with traceback. To be used in exception handlers.
    
    Args:
        msg (str): Message to log
        include_location (bool): Whether to include file/line/function info
    """
    if not _CONFIGURED:
        _auto_configure()
    logging.exception(_format_message(msg, include_location))
