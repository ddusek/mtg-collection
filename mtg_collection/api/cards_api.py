from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from redis import Redis
from redis_helpers import get_suggestions, get_all_editions
from card_helpers import format_cards, format_editions


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


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
    redis = Redis(host='localhost', port=6379, db=0)
    data = get_suggestions(redis, text, 20)
    return jsonify(format_cards(data))


@app.route('/editions')
@cross_origin()
def editions():
    """Return all editions.
    """
    redis = Redis(host='localhost', port=6379, db=0)
    data = get_all_editions(redis)
    print(data)
    data_decoded = [byte.decode('utf-8') for byte in data]
    return jsonify(format_editions(data_decoded))
