import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGGING_FILE = f"{ROOT_DIR}/data/logs.log"

# Scryfall data.
SCRYFALL_BULK_URL = "https://api.scryfall.com/bulk-data"
SCRYFALL_EDITIONS_URL = "https://api.scryfall.com/sets"
SCRYFALL_CARDS_JSON_PATH = "data/json_cards.json"

# Redis.
REDIS_HOST = "0.0.0.0"
REDIS_HOSTNAME = "mtg-redis"
REDIS_PORT = 6379
REDIS_MAIN_DB = 0

# MongoDB.
MONGO_HOST = "0.0.0.0"
MONGO_HOSTNAME = "mtg-mongo"
MONGO_DATABASE = "mtg-collection"
MONGO_USERNAME = "mtg-admin"
MONGO_PASSWORD = "123456"
