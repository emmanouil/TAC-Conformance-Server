"""
    TAC Conformance Server

    DASH-IF Implementation Guidelines: Token-based
    Access Control for DASH (TAC)
"""

import logging

def init_logging():
    """
    Initialize and return the logger.
    """
    logger = logging.getLogger(__name__)
    log_format = '[%(asctime)s] [%(levelname)s] %(message)s'
    logging.basicConfig(format=log_format, level=logging.DEBUG)
    return logger
