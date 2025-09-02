"""
Configuration file for AEDCO One Platform
Environment-based configuration with sensible defaults
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Flask Configuration
class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'aedco-dev-secret-key-2024')
    DEBUG = False
    TESTING = False
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', 'your-openai-api-key-here')
    OPENAI_MODEL = 'gpt-4'
    OPENAI_TEMPERATURE = 0.2
    OPENAI_MAX_TOKENS = 8000
    
    # File Upload Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_EXTENSIONS = {'.pdf', '.html', '.eml', '.txt'}
    
    # Newsletter Configuration
    MAX_PAST_ISSUES_PER_SECTOR = 50
    MAX_RUNS_PER_SECTOR = 100
    
    # Timezone Configuration
    DEFAULT_TIMEZONE = 'Africa/Cairo'
    
    # Brand Configuration
    BRAND_NAME = 'AEDCO'
    BRAND_FULL_NAME = 'Arab Engineering & Distribution Company'
    BRAND_COLORS = {
        'primary': '#0B3D91',
        'secondary': '#1F2937',
        'gradient': 'linear-gradient(135deg, #0B3D91 0%, #1F2937 100%)'
    }

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    OPENAI_TEMPERATURE = 0.3  # Slightly more creative for development

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    OPENAI_TEMPERATURE = 0.1  # More conservative for production
    
    # Production-specific settings
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable is required for production")

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    OPENAI_API_KEY = 'test-key'
    WTF_CSRF_ENABLED = False

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on environment."""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])

# Export configuration
current_config = get_config()