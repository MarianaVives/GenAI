"""Application settings and configuration"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Load environment variables from .env file
ENV_FILE = PROJECT_ROOT / '.env'
if ENV_FILE.exists():
    load_dotenv(ENV_FILE)
else:
    load_dotenv()

# API Configuration
API_TIMEOUT = int(os.getenv('API_TIMEOUT', '5'))  # seconds
API_RETRIES = int(os.getenv('API_RETRIES', '3'))
API_BASE_URL = os.getenv('API_BASE_URL', 'https://api.open-meteo.com')
GEOCODING_API_URL = os.getenv('GEOCODING_API_URL', 'https://geocoding-api.open-meteo.com')

# API Keys (if needed for other services)
API_KEY = os.getenv('API_KEY', '').strip()
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-key-change-in-production')

# Output format options: 'detailed' or 'simple'
OUTPUT_FORMAT = os.getenv('OUTPUT_FORMAT', 'detailed')

# Cache settings (optional)
CACHE_ENABLED = os.getenv('CACHE_ENABLED', 'False').lower() == 'true'
CACHE_DURATION = int(os.getenv('CACHE_DURATION', '600'))  # seconds

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = PROJECT_ROOT / os.getenv('LOG_FILE', 'weather_app.log')

# Flask Configuration
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
FLASK_PORT = int(os.getenv('FLASK_PORT', '5000'))
