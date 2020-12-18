from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from redis import Redis
from card_helper import format_cards, format_editions
from redis_helper import get_suggestions, get_all_editions, get_collection, get_collections

MAIN_REDIS_HOST = 'mtg-redis'
MAIN_REDIS_PORT = 6379
MAIN_REDIS_DB = 0

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
redis = Redis(host=MAIN_REDIS_HOST, port=MAIN_REDIS_PORT, db=MAIN_REDIS_DB)


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
    data = get_suggestions(redis, text, 20)
    return jsonify(format_cards(data))


@app.route('/editions')
@cross_origin()
def editions():
    """Return all editions.
    """
    data = get_all_editions(redis)
    data_decoded = [byte.decode('utf-8') for byte in data]
    return jsonify(format_editions(data_decoded))


@app.route('/collections')
@cross_origin()
def collections():
    """Return all collections.
    """
    data = get_collections(redis)
    data_decoded = [byte.decode('utf-8') for byte in data]
    return jsonify(data_decoded)


@app.route('/collection/<name>')
@cross_origin()
def collection(name):
    """Return all cards from collection by its name.
    """
    return name


@app.route('/add/<collection>/<card>/<units>')
@cross_origin()
def add_card(collection, card, units):
    """Add card to collection.
    """
    return


@app.route('/remove/<collection>/<card>/<units>')
@cross_origin()
def remove_card(collection, card, units):
    """Remove card from collection.
    """
    return


@app.route('/add/<collection>')
@cross_origin()
def add_collection(collection):
    """Add new collection.
    """
    return
