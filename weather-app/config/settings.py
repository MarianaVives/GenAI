"""Application settings and configuration"""
import os
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# API Configuration
API_TIMEOUT = 5  # seconds
API_RETRIES = 3

# Output format options: 'detailed' or 'simple'
OUTPUT_FORMAT = 'detailed'

# Cache settings (optional)
CACHE_ENABLED = False
CACHE_DURATION = 600  # seconds

# Logging
LOG_LEVEL = 'INFO'
LOG_FILE = PROJECT_ROOT / 'weather_app.log'
