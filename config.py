import os
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent  # Assuming config.py is now inside docsumm

# LLM Configuration
LLM_MODEL = os.environ.get('LLM_MODEL', 'gemma2:2b')
LLM_TEMPERATURE = float(os.environ.get('LLM_TEMPERATURE', 0))

# File Processing
MAX_CONCURRENT_FILES = int(os.environ.get('MAX_CONCURRENT_FILES', 5))
DEFAULT_ENCODING = 'utf-8'

# Logging Configuration
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = BASE_DIR / 'docsumm' / 'logs' / 'file_summarizer.log'

# Summary Generation
MAX_SUMMARY_LENGTH = int(os.environ.get('MAX_SUMMARY_LENGTH', 500))
MIN_TITLE_WORDS = int(os.environ.get('MIN_TITLE_WORDS', 5))
MAX_TITLE_WORDS = int(os.environ.get('MAX_TITLE_WORDS', 10))

# Input/Output Directories
INPUT_DIR = Path(BASE_DIR / 'docsumm' / 'doclib')
OUTPUT_DIR = Path(BASE_DIR / 'docsumm' / 'doclib')

# Error Handling
MAX_RETRIES = int(os.environ.get('MAX_RETRIES', 3))
RETRY_DELAY = float(os.environ.get('RETRY_DELAY', 1.0))  # in seconds

# Performance
CHUNK_SIZE = int(os.environ.get('CHUNK_SIZE', 1000))  # for processing large files

# API Keys (if needed)
# OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# Debug Mode
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# Ensure required directories exist
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOG_FILE.parent, exist_ok=True)
