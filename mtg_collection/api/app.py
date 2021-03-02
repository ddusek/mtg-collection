import json
import urllib.parse
from redis import Redis
from pymongo import MongoClient
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.responses import JSONResponse
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from mtg_collection import constants
from mtg_collection.api import logger
from mtg_collection.database import redis_helper
from mtg_collection.database.download import Downloader
from mtg_collection.database.synchronize import Synchronizer
from mtg_collection.database.authentication import Authenticator


async def register(request) -> JSONResponse:
    """Register a new user and save him into a session.

    :return: {"success": bool}.
    :rtype: JSONResponse
    """
    params = await request.json()
    auth = Authenticator(MONGO)
    success = auth.register_user(params['username'], params['password'], params['email'])
    return JSONResponse({'success': success[0], 'message': success[1]})


async def login(request) -> JSONResponse:
    """Login user and save him into a session.

    :return: {"success": bool}.
    :rtype: JSONResponse
    """
    pass


async def suggest(request) -> JSONResponse:
    """Return auto suggested cards.

    :param text: Text which cards need to contain.
    :type text: str
    :return: List of cards.
    :rtype: JSONResponse
    """
    text = request.path_params['text']
    try:
        data = redis_helper.get_suggestions(REDIS, text, 20)
        result = redis_helper.format_cards(data)
        return JSONResponse(result)
    except (ConnectionError, TimeoutError) as err:
        logger.exception(err)
    except IndexError as err:
        logger.exception(err)
    except TypeError as err:
        logger.exception(err)


async def editions(request) -> JSONResponse:
    """Return all editions.

    :return: List of all editions.
    :rtype: JSONResponse
    """
    try:
        data = redis_helper.get_all_editions(REDIS)
        data_decoded = [byte.decode('utf-8').removeprefix('edition:') for byte in data]
        result = redis_helper.format_dropdown(data_decoded)
        if result is None:
            logger.warning('\'/editions\' returned 0 values')
        return JSONResponse(result)
    except (ConnectionError, TimeoutError) as err:
        logger.exception('cannot connect to Redis. %s', err)


async def collections(request) -> JSONResponse:
    """Return all collections.

    :return: List of collections.
    :rtype: JSONResponse
    """
    try:
        data = redis_helper.get_all_collections(REDIS)
        data_decoded = [byte.decode('utf-8') for byte in data]
        result = redis_helper.format_set_dropdown(data_decoded)
        return JSONResponse(result)
    except (ConnectionError, TimeoutError) as err:
        logger.exception('cannot connect to Redis. %s', err)


async def collection(request) -> JSONResponse:
    """Return all cards from collection by its name.

    :param name: Collection key in Redis.
    :type name: str
    :return: List of card objects.
    :rtype: JSONResponse
    """
    name = request.path_params['name']
    try:
        data = redis_helper.get_collection(REDIS, name)
        data_decoded = [json.loads(byte.decode('utf-8')) for byte in data]

        result = []
        # Add index, so there is a better value to set as key in Vue loops.
        for i, item in enumerate(data_decoded):
            item['id'] = i
            result.append(item)
        return JSONResponse(result)
    except (ConnectionError, TimeoutError) as err:
        logger.exception('cannot connect to Redis. %s', err)


async def add_card(request) -> JSONResponse:
    """Add card to collection.

    :param collection: Collection key in Redis, where card should be saved.
    :type collection: str
    :param card: Card part of key in Redis.
    :type card: str
    :param edition: Edition part of card key in Redis.
    :type edition: str
    :param units: Number of units to save.
    :type units: int
    :return: {"success": bool}.
    :rtype: JSONResponse
    """
    collection = request.path_params['collection']
    card = request.path_params['card']
    edition = request.path_params['edition']
    units = request.path_params['units']
    try:
        result = redis_helper.add_card_to_redis(REDIS, collection, card, edition, units)
        return JSONResponse(result)
    except ValueError as err:
        logger.exception(err)
    except (ConnectionError, TimeoutError) as err:
        logger.exception('cannot connect to Redis. %s', err)


async def remove_card(request) -> JSONResponse:
    """Remove card from collection.

    param collection: Collection key in Redis, from where to remove card.
    :type collection: str
    :param card: Card part of key in Redis.
    :type card: str
    :param edition: Edition part of card key in Redis.
    :type edition: str
    :param units: Number of units to remove.
    :type units: int
    :return: {"success": bool}.
    :rtype: JSONResponse
    """
    # collection = request.path_params['collection']
    # card = request.path_params['card']
    # edition = request.path_params['edition']
    # units = request.path_params['units']
    return


async def add_collection(request) -> JSONResponse:
    """Add new collection.

    :param collection: Collection key to add to Redis.
    :type collection: str
    :return: {"success": bool}.
    :rtype: JSONResponse
    """
    collection = request.path_params['collection']
    try:
        result = redis_helper.add_collection_to_redis(REDIS, collection)
        return JSONResponse(result)
    except (ConnectionError, TimeoutError) as err:
        logger.exception('cannot connect to Redis. %s', err)


async def download_scryfall_cards(request) -> JSONResponse:
    """Download cards bulk data from Scryfall.

    :return: {"success": bool}.
    :rtype: JSONResponse
    """
    result = Downloader().download_scryfall_cards()
    return JSONResponse({'success': result})


async def synchronize_scryfall_cards(request) -> JSONResponse:
    """Synchronize cards from Scryfall to redis.

    :return: {"success": bool}.
    :rtype: JSONResponse
    """
    result = Synchronizer(REDIS).synchronize_database()
    return JSONResponse({'success': result})


middleware = [Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['GET', 'POST'])]
routes = [
    Mount('/api', routes=[
        Route('/register', register, methods=['POST', 'OPTIONS']),
        Route('/login', login, methods=['POST']),
        Route('/suggest/{text:str}', suggest),
        Route('/editions', editions),
        Route('/collections', collections),
        Route('/collection/{name:str}', collection),
        Route('/add/{collection:str}/{card:str}/{edition:str}/{units:int}', add_card, methods=['POST']),
        Route('/remove/{collection:str}/{card:str}/{edition:str}/{units:int}', remove_card),
        Route('/add/{collection}', add_collection, methods=['POST']),
        Route('/download/scryfall/cards', download_scryfall_cards),
        Route('/synchronize/scryfall/cards', synchronize_scryfall_cards),
    ])
]
app = Starlette(debug=True, middleware=middleware, routes=routes)
REDIS = Redis(host=constants.REDIS_HOSTNAME, port=constants.REDIS_PORT, db=constants.REDIS_MAIN_DB)
MONGO = MongoClient('mongodb://%s:%s@%s' % (
                    urllib.parse.quote_plus(constants.MONGO_USERNAME),
                    urllib.parse.quote_plus(constants.MONGO_PASSWORD),
                    constants.MONGO_HOSTNAME),
                    serverSelectionTimeoutMS=3000)['mtg-collection']
