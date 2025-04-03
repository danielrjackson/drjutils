"""
Tests for the enhanced schema parser.

This tests the schema parser with constants, validators, templates, and the range syntax.
"""

import re
import unittest
from pathlib import Path
from datetime import datetime

import pytest
pytest.skip("WIP - not ready yet", allow_module_level=True)


# Import the schema parser
from libs.drjutils.config.schema_parser import SchemaParser, parse_schema_dict
from libs.drjutils.config.schema import ConfigSchema, ConfigSchemaEntry
from libs.drjutils.log import configure

class SchemaParserTest(unittest.TestCase):
    """Test case for the schema parser."""
    
    def setUp(self):
        """Set up the test case."""
        # Configure logging
        configure()
        
        # Create a test schema with all features
        self.test_schema = {
            # Constants section
            'constants': {
                'MAX_PORT': 65535,
                'MIN_PORT': 1024,
                'DEFAULT_TIMEOUT': 30,
                'SERVICE_URL': 'https://api.example.com'
            },
            
            # Validators section
            'validators': {
                'port_range': '1024..65535',
                'timeout_range': [0, 3600],
                'email_pattern': r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            },
            
            # Templates section
            'templates': {
                'api_credential': {
                    'format': 'str',
                    'required': True,
