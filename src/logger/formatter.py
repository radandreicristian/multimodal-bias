import logging
from logging import Formatter


class CustomFormatter(Formatter):
    """A custom log formatter that adds a field with the initial of the log's level."""

    def format(self, record: logging.LogRecord) -> str:
        """Format a custom log record by adding a new field with the initial of the logging letter.

        Args:
            record: A logging record.

        Returns: The logging record with the updated field.
        """
        record.levelname_initial = record.levelname[0]
        record.filename = record.filename.split(".")[0]
        log_message = super(CustomFormatter, self).format(record)
        return log_message
