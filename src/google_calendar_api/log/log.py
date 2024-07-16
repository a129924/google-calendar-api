from logging import StreamHandler, getLogger
from sys import stdout

__all__ = ["LOGGER"]

log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOGGER = getLogger(__name__)

LOGGER.addHandler(StreamHandler(stdout))
