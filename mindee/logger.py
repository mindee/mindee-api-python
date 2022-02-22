"""
Set up a logger.
"""

import os
import logging

LOGLEVEL = os.environ.get("MINDEE_LOGLEVEL", "INFO").upper()
logging.basicConfig(level=LOGLEVEL)

logger = logging.getLogger("mindee")
