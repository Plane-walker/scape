DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
    },
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s'
        },
        'short': {
            'format': '%(asctime)s %(levelname)s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'short'
        }
    },
    'loggers': {
        'scape': {
            'handlers': ['console'],
            'level': 'DEBUG'
        }
    }
}

INNER_EXECUTORS = [
    'scape.action.inner_executor.Delayer',
    'scape.action.inner_executor.Activator'
]
