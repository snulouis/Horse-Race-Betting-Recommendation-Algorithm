"""
Logging error to file, print debug log.
"""
import logging


logger = logging.getLogger('Crawler')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('error.log')
fh.setLevel(logging.ERROR)
fh.setFormatter(logging.Formatter('%(asctime)s | %(lineno)d | %(message)s'))
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)

logger.addHandler(fh)
logger.addHandler(sh)

def print_debug(*msg):
    logger.debug(*msg)

def print_error(*msg):
    logger.error(*msg)