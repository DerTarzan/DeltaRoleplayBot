import os
import logging
from typing import Dict
from logging.handlers import RotatingFileHandler

class LoggerConfig:
    def __init__(self):
        self.log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'logs')

class Logger(LoggerConfig):
    _loggers: Dict[str, logging.Logger] = {}

    def __init__(self, logger_name: str, log_level: int = logging.DEBUG, create_file_handler: bool = True):
        super().__init__()

        if logger_name in self._loggers:
            self.logger = self._loggers[logger_name]
        else:
            self.logger = logging.getLogger(logger_name)
            self.logger.setLevel(log_level)
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

            os.makedirs(self.log_path, exist_ok=True)

            if create_file_handler:
                file_handler = RotatingFileHandler(
                    os.path.join(self.log_path, f"{logger_name}.log"),
                    encoding="utf-8"
                )
                file_handler.setLevel(log_level)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)

            root_handler = RotatingFileHandler(
                os.path.join(self.log_path, f"{__name__}.log"),
                encoding="utf-8"
            )
            root_handler.setLevel(log_level)
            root_handler.setFormatter(formatter)
            self.logger.addHandler(root_handler)

            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

            self._loggers[logger_name] = self.logger

    def get_logger(self) -> logging.Logger:
        return self.logger