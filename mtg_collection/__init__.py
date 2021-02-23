import logging
from mtg_collection import constants

logging.FileHandler(filename=constants.LOGGING_FILE, mode='w', encoding='utf-8')
logging.basicConfig(filename=constants.LOGGING_FILE, encoding='utf-8', level=logging.WARNING)
logger = logging.getLogger()
