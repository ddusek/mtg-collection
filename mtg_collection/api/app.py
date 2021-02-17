import json
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from redis import Redis
from mtg_collection import constants
from mtg_collection.database import redis_helper
from mtg_collection.database import download
from mtg_collection.database import synchronize

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
REDIS = Redis(host=constants.REDIS_HOSTNAME, port=constants.REDIS_PORT, db=constants.REDIS_MAIN_DB)


@app.route('/suggest/<text>')
@cross_origin()
def suggest(text: str) -> object:
    """Return auto suggested cards.

    :param text: Text which cards need to contain.
    :type text: str
    :return: List of cards.
    :rtype: object
    """
    data = redis_helper.get_suggestions(REDIS, text, 20)
    return jsonify(redis_helper.format_cards(data))


@app.route('/editions')
@cross_origin()
def editions() -> object:
    """Return all editions.

    :return: List of all editions.
    :rtype: object
    """
    data = redis_helper.get_all_editions(REDIS)
    data_decoded = [byte.decode('utf-8') for byte in data]
    return jsonify(redis_helper.format_dropdown(data_decoded))


@app.route('/collections')
@cross_origin()
def collections() -> object:
    """Return all collections.

    :return: List of collections.
    :rtype: object
    """
    data = redis_helper.get_all_collections(REDIS)
    data_decoded = [byte.decode('utf-8') for byte in data]
    return jsonify(redis_helper.format_set_dropdown(data_decoded))


@app.route('/collection/<name>')
@cross_origin()
def collection(name: str) -> object:
    """Return all cards from collection by its name.

    :param name: Collection key in Redis.
    :type name: str
    :return: List of card objects.
    :rtype: object
    """
    data = redis_helper.get_collection(REDIS, name)
    data_decoded = [json.loads(byte.decode('utf-8')) for byte in data]

    indexed = []
    # Add index, so there is a better value to set as key in Vue loops.
    for i, item in enumerate(data_decoded):
        item['id'] = i
        indexed.append(item)
    return jsonify(indexed)


@app.route('/add/<collection>/<card>/<units>', methods=['POST'])
@cross_origin()
def add_card(collection: str, card: str, units: int) -> object:
    """Add card to collection.

    :param collection: Collection key in Redis, where card should be saved.
    :type collection: str
    :param card: Card key in Redis.
    :type card: str
    :param units: Number of units to save.
    :type units: int
    :return: {"success": bool}.
    :rtype: object
    """
    return jsonify(redis_helper.add_card_to_redis(REDIS, collection, card, units))


@app.route('/remove/<collection>/<card>/<units>')
@cross_origin()
def remove_card(collection: str, card: str, units: int) -> object:
    """Remove card from collection.

    param collection: Collection key in Redis, from where to remove card.
    :type collection: str
    :param card: Card key in Redis.
    :type card: str
    :param units: Number of units to remove.
    :type units: int
    :return: {"success": bool}.
    :rtype: object
    """
    return


@app.route('/add/<collection>', methods=['POST'])
@cross_origin()
def add_collection(collection: str) -> object:
    """Add new collection.

    :param collection: Collection key to add to Redis.
    :type collection: str
    :return: {"success": bool}.
    :rtype: object
    """
    return jsonify(redis_helper.add_collection_to_redis(REDIS, collection))


@app.route('/download/scryfall/cards')
@cross_origin()
def download_scryfall_cards() -> object:
    """Download cards bulk data from Scryfall.

    :return: {"success": bool}.
    :rtype: object
    """
    result = download.Downloader().download_scryfall_cards()
    return jsonify({'success': result})


@app.route('/synchronize/scryfall/cards')
@cross_origin()
def synchronize_scryfall_cards() -> object:
    """Synchronize cards from Scryfall to redis.

    :return: {"success": bool}.
    :rtype: object
    """
    result = synchronize.Synchronizer(REDIS).synchronize_database()
    return jsonify({'success': result})
