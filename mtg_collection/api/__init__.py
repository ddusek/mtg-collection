import logging
from mtg_collection import constants

logging.basicConfig(filename=constants.LOGGING_FILE, filemode='a', encoding='utf-8', level=logging.WARNING)
logger = logging.getLogger(__name__)
