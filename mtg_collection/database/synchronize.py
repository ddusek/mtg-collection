"""Redis structure
Database currently contains all cards, all sets and all created collections.


key, value

cards
card:<edition>:<name>, <dictionary_values>

sets
edition:<edition>, <dictionary_values>

my collections
collection:<collection_name>, <collection_name>

My cards
<collection_name>:<name>, <dictinary_values>
"""
import json
from pathlib import Path
from redis import Redis
import requests


class Synchronize():
    """Init or sync Redis database from json file.
    """
    file_path = "../fetch/json_cards.json"
    editions_url = 'https://api.scryfall.com/sets'

    def __init__(self, host, port, db):
        self.redis = Redis(host=host, port=port, db=db)
        self.cards = []

    def _json_to_dict(self):
        """Get file into list of every line.
        """
        path = Path(__file__).parent / self.file_path
        with open(path, 'r') as file:
            self.cards = json.load(file)

    def _filter_card_fields(self, card):
        """Create card key and get only wanted card fields as value.
        """
        key = f'card:{card["set_name"].lower().replace(":", ";")}: \
        {card["name"].lower().replace(":", ";")}'
        values = {
            'name': card['name'],
            'set': card['set_name'],
            'price': card['prices']['usd'],
            'price_foil': card['prices']['usd_foil'],
            'release': card['released_at'],
        }
        return ({'key': key, 'value': values})

    def _filter_edition_fields(self, edition):
        """Create edition key and get only wanted edition fields as value.
        """
        key = f'edition:{edition["name"].lower().replace(":", ";")}'
        values = {
            'image': edition['icon_svg_uri'],
            'name': edition['name'],
            'released': edition['released_at']
        }
        return ({'key': key, 'value': values})

    def _init_editions(self):
        """Save all editions in db.
        """
        response = requests.get(self.editions_url)
        editions = response.json()
        for edition in editions['data']:
            if edition is not None:
                self._write_record(self._filter_edition_fields(edition), 'edition')
        self.redis.bgsave()
        print('done sets')

    def _init_cards(self):
        """Save all cards in db.
        """
        self._json_to_dict()
        for card in self.cards:
            if card is not None:
                self._write_record(self._filter_card_fields(card), 'card')
        self.redis.bgsave()

    def _write_record(self, obj, set_name=None):
        """Write record from json to database.

        :param obj: obj to write.
        :param set_name: if not None, add obj['key'] to this set. Defaults to None
        """
        self.redis.set(obj['key'], json.dumps(obj['value']))
        if set_name is not None:
            self.redis.sadd(set_name, obj['key'])

    def _delete_by_pattern(self, pattern):
        """Delete all keys in given pattern.
        """
        matched_keys = []
        cur = '0'
        while cur != 0:
            cur, keys = self.redis.scan(cur, pattern, 10000)
            matched_keys += keys
        if len(matched_keys) > 0:
            for key in matched_keys:
                self.redis.delete(key)

    def init_db(self):
        """Initialize Redis database and load all cards.
        """
        self._delete_by_pattern('edition:*')
        self._delete_by_pattern('card:*')
        self._init_cards()
        self._init_editions()
        print('done init database')


class RedisSyncCollections():
    """Sync collections prices.
    """
    def __init__(self, host, port, db):
        self.redis = Redis(host=host, port=port, db=db)


synchronizer = Synchronize(host='0.0.0.0', port=6379, db=0)
synchronizer.init_db()
