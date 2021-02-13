from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from redis import Redis
from database import redis_helper
import constants

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
REDIS = Redis(host=constants.REDIS_HOSTNAME, port=constants.REDIS_PORT, db=constants.REDIS_MAIN_DB)
# REDIS = Redis(host='0.0.0.0', port=6379, db=0)


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
    data = redis_helper.get_suggestions(REDIS, text, 20)
    return jsonify(redis_helper.format_cards(data))


@app.route('/editions')
@cross_origin()
def editions():
    """Return all editions.
    """
    data = redis_helper.get_all_editions(REDIS)
    data_decoded = [byte.decode('utf-8') for byte in data]
    return jsonify(redis_helper.format_dropdown(data_decoded))


@app.route('/collections')
@cross_origin()
def collections():
    """Return all collections.
    """
    print(Redis)
    data = redis_helper.get_all_collections(REDIS)
    data_decoded = [byte.decode('utf-8') for byte in data]
    return jsonify(redis_helper.format_set_dropdown(data_decoded))


@app.route('/collection/<name>')
@cross_origin()
def collection(name):
    """Return all cards from collection by its name.
    """
    data = redis_helper.get_collection(REDIS, name)
    data_decoded = [byte.decode('utf-8') for byte in data]
    return jsonify(data_decoded)


@app.route('/add/<collection>/<card>/<units>', methods=['POST'])
@cross_origin()
def add_card(collection, card, units):
    """Add card to collection.
    """
    return jsonify(redis_helper.add_card_to_redis(REDIS, collection, card, units))


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
    return jsonify(redis_helper.add_collection_to_redis(REDIS, collection))
