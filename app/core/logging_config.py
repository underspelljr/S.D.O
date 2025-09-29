import logging.config
from app.core.config import settings

def setup_logging():
    """
    Set up the application logging configuration.
    """
    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
        },
        'handlers': {
            'console': {
                'level': settings.LOG_LEVEL,
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
            },
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['console'],
                'level': settings.LOG_LEVEL,
                'propagate': True,
            },
            'uvicorn.error': {
                'level': 'INFO',
            },
            'uvicorn.access': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
        }
    }
    logging.config.dictConfig(LOGGING_CONFIG)