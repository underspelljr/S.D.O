import logging
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
    """
    Application settings loaded from .env file.
    """
    APP_NAME: str = "Spots de Oeiras"
    LOG_LEVEL: str = "INFO"
    DATABASE_URL: str = "sqlite:///./spots_de_oeiras.db"

    # Pydantic V2 configuration to read from the .env file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')

# Create a single instance of the settings to be imported across the application
settings = AppSettings()

# Validate LOG_LEVEL after loading settings
log_level_numeric = getattr(logging, settings.LOG_LEVEL.upper(), None)
if not isinstance(log_level_numeric, int):
    raise ValueError(f'Invalid log level: {settings.LOG_LEVEL}')