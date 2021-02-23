import json
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from redis import Redis
from mtg_collection import constants
from mtg_collection.api import logger
from mtg_collection.database import redis_helper
from mtg_collection.database.download import Downloader
from mtg_collection.database.synchronize import Synchronizer

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
    try:
        data = redis_helper.get_suggestions(REDIS, text, 20)
        result = redis_helper.format_cards(data)
        return jsonify(result)
    except (ConnectionError, TimeoutError) as err:
        logger.exception(err)
    except IndexError as err:
        logger.exception(err)
    except TypeError as err:
        logger.exception(err)


@app.route('/editions')
@cross_origin()
def editions() -> object:
    """Return all editions.

    :return: List of all editions.
    :rtype: object
    """
    try:
        data = redis_helper.get_all_editions(REDIS)
        data_decoded = [byte.decode('utf-8').removeprefix('edition:') for byte in data]
        result = redis_helper.format_dropdown(data_decoded)
        if result is None:
            logger.warning('\'/editions\' returned 0 values')
        return jsonify(result)
    except (ConnectionError, TimeoutError) as err:
        logger.exception('cannot connect to Redis. %s', err)


@app.route('/collections')
@cross_origin()
def collections() -> object:
    """Return all collections.

    :return: List of collections.
    :rtype: object
    """
    try:
        data = redis_helper.get_all_collections(REDIS)
        data_decoded = [byte.decode('utf-8') for byte in data]
        result = redis_helper.format_set_dropdown(data_decoded)
        return jsonify(result)
    except (ConnectionError, TimeoutError) as err:
        logger.exception('cannot connect to Redis. %s', err)


@app.route('/collection/<name>')
@cross_origin()
def collection(name: str) -> object:
    """Return all cards from collection by its name.

    :param name: Collection key in Redis.
    :type name: str
    :return: List of card objects.
    :rtype: object
    """
    try:
        data = redis_helper.get_collection(REDIS, name)
        data_decoded = [json.loads(byte.decode('utf-8')) for byte in data]

        result = []
        # Add index, so there is a better value to set as key in Vue loops.
        for i, item in enumerate(data_decoded):
            item['id'] = i
            result.append(item)
        return jsonify(result)
    except (ConnectionError, TimeoutError) as err:
        logger.exception('cannot connect to Redis. %s', err)


@app.route('/add/<collection>/<card>/<edition>/<units>', methods=['POST'])
@cross_origin()
def add_card(collection: str, card: str, edition: str, units: int) -> object:
    """Add card to collection.

    :param collection: Collection key in Redis, where card should be saved.
    :type collection: str
    :param card: Card part of key in Redis.
    :type card: str
    :param edition: Edition part key of card key in Redis.
    :type edition: str
    :param units: Number of units to save.
    :type units: int
    :return: {"success": bool}.
    :rtype: object
    """
    try:
        result = redis_helper.add_card_to_redis(REDIS, collection, card, edition, units)
        return jsonify(result)
    except ValueError as err:
        logger.exception(err)
    except (ConnectionError, TimeoutError) as err:
        logger.exception('cannot connect to Redis. %s', err)


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
    try:
        result = redis_helper.add_collection_to_redis(REDIS, collection)
        return jsonify(result)
    except (ConnectionError, TimeoutError) as err:
        logger.exception('cannot connect to Redis. %s', err)


@app.route('/download/scryfall/cards')
@cross_origin()
def download_scryfall_cards() -> object:
    """Download cards bulk data from Scryfall.

    :return: {"success": bool}.
    :rtype: object
    """
    result = Downloader().download_scryfall_cards()
    return jsonify({'success': result})


@app.route('/synchronize/scryfall/cards')
@cross_origin()
def synchronize_scryfall_cards() -> object:
    """Synchronize cards from Scryfall to redis.

    :return: {"success": bool}.
    :rtype: object
    """
    result = Synchronizer(REDIS).synchronize_database()
    return jsonify({'success': result})
