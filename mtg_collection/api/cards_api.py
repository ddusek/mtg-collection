from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from redis import Redis
from redis_helpers import scan_all
from card_helpers import format_cards


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
    data = scan_all(redis, text, 20)
    # data = [byte.decode('utf-8') for byte in keys]
    return jsonify(format_cards(data))
