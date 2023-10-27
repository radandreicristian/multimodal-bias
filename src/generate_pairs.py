import json
import logging.config
import os

from dotenv import dotenv_values

from src.logger.utils import get_logging_config

config = {**dotenv_values("src/config/.env"), **os.environ}

logging.config.dictConfig(json.load(open(get_logging_config(**config))))

logger = logging.getLogger()


def generate_pairs():
    for method in (logger.debug, logger.info, logger.warning, logger.error, logger.critical):
        method("Generating pairs")


if __name__ == "__main__":
    generate_pairs()
