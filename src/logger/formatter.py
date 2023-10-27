import logging
from logging import Formatter


class CustomFormatter(Formatter):
    def format(self, record: logging.LogRecord) -> str:
        record.levelname_initial = record.levelname[0]
        record.filename = record.filename.split(".")[0]
        log_message = super(CustomFormatter, self).format(record)
        return log_message
