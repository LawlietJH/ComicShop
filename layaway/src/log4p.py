from shared.infrastructure.settings import get_settings

settings = get_settings()

config = {
    'monitorInterval': 10,
    'loggers': {
        'root': {
            'level': 'INFO',
            'AppenderRef': [settings.APPENDERS]
        }
    },
    'appenders': {
        'file': {
            'type': 'file',
            'FileName': 'service.log',
            'backup_count': 5,
            'file_size_limit': 1024 * 1024 * 500,
            'PatternLayout': "%(message)s"
        },
        'console': {
            'type': 'console',
            'target': 'console',
            'PatternLayout': "%(message)s"
        }
    }
}
