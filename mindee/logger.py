"""Set up a logger."""

import logging
import os

LOGLEVEL = os.environ.get("MINDEE_LOGLEVEL", "WARNING").upper()
logging.basicConfig(level=LOGLEVEL)

logger = logging.getLogger("mindee")
