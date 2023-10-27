import logging


class LogLevelInitialFilter(logging.Filter):
    def filter(self, record):
        # Create a custom attribute 'levelname_initial' with the log level's initial
        record.levelname_initial = record.levelname[0]
        return True


class LogLevelInitialLogRecord(logging.LogRecord):
    def __init__(self, *args, **kwargs):
        super(LogLevelInitialLogRecord, self).__init__(*args, **kwargs)
        self.levelname_initial = kwargs.get("levelname_initial", "")


# Create a custom LogRecord factory
class LogLevelInitialLogRecordFactory(logging.getLogRecordFactory()):
    def __call__(self, *args, **kwargs):
        return LogLevelInitialLogRecord(*args, **kwargs)
