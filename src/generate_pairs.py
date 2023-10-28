import json
import logging.config
import os

from dotenv import dotenv_values

from src.caption.generator import CaptionGenerator
from src.logger.utils import get_logging_config

config = {**dotenv_values("src/config/.env"), **os.environ}

logging.config.dictConfig(json.load(open(get_logging_config(config))))

logger = logging.getLogger()


if __name__ == "__main__":
    t = "A little boy in kimono meditation before aikido competition in sports hall."
    g = CaptionGenerator()
    s = g.get_subject(t)
    print(s)
