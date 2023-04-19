import logging
from logging.config import dictConfig

from shared.config import settings


dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] [%(levelname)s] %(message)s',
        },
    },
    'handlers': {
        'console': {
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': settings['APP_LOG_LEVEL'],
    },
    'command_coach': {
        'handlers': ['console'],
        'level': settings['APP_LOG_LEVEL'],
    },
})


logging = logging
