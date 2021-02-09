from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from redis import Redis
from card_helper import format_cards, format_dropdown
from redis_helper import (get_suggestions, get_all_editions, get_all_collections, get_collection,
                          add_card_to_redis, add_collection_to_redis)

MAIN_REDIS_HOST = 'mtg-redis'
MAIN_REDIS_PORT = 6379
MAIN_REDIS_DB = 0

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
REDIS = Redis(host=MAIN_REDIS_HOST, port=MAIN_REDIS_PORT, db=MAIN_REDIS_DB)


@app.route('/')
@cross_origin()
def hello_world():
    """Just for test functionality.
    """
    return 'hello world'


@app.route('/suggest/<text>')
@cross_origin()
def suggest(text):
    """Return auto suggested cards.
    """
    data = get_suggestions(REDIS, text, 20)
    return jsonify(format_cards(data))


@app.route('/editions')
@cross_origin()
def editions():
    """Return all editions.
    """
    data = get_all_editions(REDIS)
    data_decoded = [byte.decode('utf-8') for byte in data]
    return jsonify(format_dropdown(data_decoded))


@app.route('/collections')
@cross_origin()
def collections():
    """Return all collections.
    """
    data = get_all_collections(REDIS)
    data_decoded = [byte.decode('utf-8') for byte in data]
    return jsonify(format_dropdown(data_decoded))


@app.route('/collection/<name>')
@cross_origin()
def collection(name):
    """Return all cards from collection by its name.
    """
    data = get_collection(REDIS, name)
    data_decoded = [byte.decode('utf-8') for byte in data]
    return jsonify(data_decoded)


@app.route('/add/<collection>/<card>/<units>', methods=['POST'])
@cross_origin()
def add_card(collection, card, units):
    """Add card to collection.
    """
    return jsonify(add_card_to_redis(REDIS, collection, card, units))


@app.route('/remove/<collection>/<card>/<units>')
@cross_origin()
def remove_card(collection, card, units):
    """Remove card from collection.
    """
    return


@app.route('/add/<collection>', methods=['POST'])
@cross_origin()
def add_collection(collection):
    """Add new collection.
    """
    return jsonify(add_collection_to_redis(REDIS, collection))
