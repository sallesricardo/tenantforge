import logging
import json
from datetime import datetime


class JsonFormatter(logging.Formatter):
    def format(self, record):
        # Create a dictionary of the log data
        log_record = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Include exception info if available
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        # Include extra contextual attributes passed via logger.info("...", extra=...)
        if hasattr(record, "extra_fields"):
            log_record.update(record.extra_fields)

        return json.dumps(log_record)


class LoggerSetup(object):
    instance = None
    LOG_LEVELS = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }

    def __init__(self, app_name, log_level: str = "INFO"):
        self.logger = logging.getLogger(app_name)
        self.logger.setLevel(self.LOG_LEVELS[log_level])
        handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter())
        self.logger.addHandler(handler)

        LoggerSetup.instance = self.logger

    @staticmethod
    def getInstance():
        return LoggerSetup.instance
