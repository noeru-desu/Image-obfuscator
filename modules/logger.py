from logging import StreamHandler, getLogger

from colorlog import ColoredFormatter


console_fmt = ColoredFormatter(
    '[%(asctime)s] [%(threadName)s] [%(log_color)s%(levelname)s%(reset)s]: '
    '%(message_log_color)s%(message)s%(reset)s',
    log_colors={
        'DEBUG': 'blue',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    },
    secondary_log_colors={
        'message': {
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red'
        }
    },
    datefmt='%H:%M:%S'
)


class Logger:
    def __init__(self, logger_registered_name: str = 'logger', initial_level: int = 20):
        self.logger = getLogger(logger_registered_name)
        self.logger.setLevel(initial_level)

        # Console Handler
        self.ch = StreamHandler()
        self.ch.setFormatter(console_fmt)
        self.logger.addHandler(self.ch)
        self.logger.warning('You are using Image encryptor BETA 2')
        self.logger.warning('Open source at https://github.com/noeru-desu/Image-encryptor')
        self.ch.setLevel(initial_level)

        self.debug = self.logger.debug
        self.info = self.logger.info
        self.warning = self.logger.warning
        self.error = self.logger.error
        self.critical = self.logger.critical
        self.exception = self.logger.exception

    def set_level(self, level: int):
        self.logger.setLevel(level)
        self.ch.setLevel(level)

    def get_logger(self):
        return self.logger
