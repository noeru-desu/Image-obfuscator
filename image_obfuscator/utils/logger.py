"""
Author       : noeru_desu
Date         : 2021-08-28 18:35:58
LastEditors  : noeru_desu
LastEditTime : 2022-07-15 17:45:10
"""
if __debug__:
    from logging import StreamHandler, getLogger

    from colorlog import ColoredFormatter


    class Logger(object):
        __slots__ = ('logger', 'ch', 'debug', 'info', 'warning', 'error', 'critical', 'exception')

        def __init__(self, logger_registered_name: str = 'logger', initial_level: int = 20, debug_format=False):
            self.logger = getLogger(logger_registered_name)
            self.logger.setLevel(initial_level)

            # Console Handler
            self.ch = StreamHandler()

            self.ch.setFormatter(self.console_fmt(debug_format))
            self.logger.addHandler(self.ch)
            self.ch.setLevel(initial_level)

            self.debug = self.logger.debug
            self.info = self.logger.info
            self.warning = self.logger.warning
            self.error = self.logger.error
            self.critical = self.logger.critical
            self.exception = self.logger.exception

        def console_fmt(self, debug_format):
            if debug_format:
                info_format = '[%(relativeCreated)d] [%(module)s] [%(lineno)s]'
                datefmt = None
            else:
                info_format = '[%(asctime)s]'
                datefmt = '%H:%M:%S'
            return ColoredFormatter(
                f'{info_format} [%(log_color)s%(levelname)s%(reset)s] %(message_log_color)s%(message)s%(reset)s',
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
                datefmt=datefmt
            )

        def set_level(self, level: int):
            self.logger.setLevel(level)
            self.ch.setLevel(level)

        def remove(self):
            self.logger.removeHandler(self.ch)
else:
    class Logger(object):
        def __init__(self, *_) -> None: pass
        def debug(self, *_): pass
        def info(self, *_): pass
        def warning(self, *_): pass
        def error(self, *_): pass
        def critical(self, *_): pass
        def exception(self, *_): pass
