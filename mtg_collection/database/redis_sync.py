"""Redis structure
Database currently contains all cards, all sets and all created collections.
key, value
cards
card:<collection>:<name>, <dictionary_values>
sets
edition:<collection>, <dictionary_values>
collection
collection:<collection_name>, <dictionary_values>

My cards
<custom_name(deck, whole_collection)>:<collection>:<name>, <dictinary_values>
"""
import sys
import json
from pathlib import Path
from redis import Redis
import requests
from .models import RedisObject


class RedisSyncDB():
    """Init or sync Redis database from json file.
    """
    def __init__(self, host, port, db):
        self.redis = Redis(host=host, port=port, db=db)
        self.lines = []
        self.lines_len = 0

    def __print_progress(self, i):
        if i % 1000 == 0:
            print(f'{format((i / self.lines_len * 100), ".2f")}% cards filled out of {self.lines_len} records')
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")

    def _get_lines(self):
        """Get file into list of every line.
        """
        path = Path(__file__).parent / "../fetch/json_cards.json"
        with open(path, 'r') as input_file:
            self.lines = input_file.readlines()
            self.lines_len = len(self.lines)-2

    def _card_as_object(self, line):
        """Return card object.

        For first and last line of file, return None.
        If There was some error with loading json, also return None.
        """
        if line == '[\n' or line == ']':
            return None
        if line[-2:] == ',\n':
            line = line[:-2]
        try:
            card_json = json.loads(line, strict=False)
            if 'set_name' not in card_json or 'name' not in card_json:
                return None
            # replace ':' because its used in redis as a key separator
            key = f'card:{card_json["set_name"].lower().replace(":", ";")}: \
                {card_json["name"].lower().replace(":", ";")}'
            selected_value = {
                'name': card_json['name'],
                'set': card_json['set_name'],
                'price': card_json['prices']['usd'],
                'price_foil': card_json['prices']['usd_foil'],
                'release': card_json['released_at'],
            }
            value = json.dumps(selected_value)
            return RedisObject(key, value)
        except json.JSONDecodeError as err:
            print(err)
            return None
        except ValueError as err:
            print(err)
            return None

    def _set_as_object(self, edition):
        """Return set object.
        """
        try:
            key = f'edition:{edition["name"].lower().replace(":", ";")}'
            selected_values = {
                'image': edition['icon_svg_uri'],
                'name': edition['name'],
                'released': edition['released_at']
            }
            value = json.dumps(selected_values)
            return RedisObject(key, value)
        except json.JSONDecodeError as err:
            print(err)
            return None
        except ValueError as err:
            print(err)
            return None

    def _init_sets(self):
        """Save all sets in db.
        """
        response = requests.get('https://api.scryfall.com/sets')
        sets = response.json()
        for _, edition in enumerate(sets['data']):
            _set = self._set_as_object(edition)
            if _set is None:
                continue
            self._write_record(_set)
        self.redis.bgsave()
        print('done sets')

    def _init_cards(self):
        """Save all cards in db.
        """
        self._get_lines()
        for i, line in enumerate(self.lines):
            self.__print_progress(i)
            card = self._card_as_object(line)
            if card is not None:
                self._write_record(card)
        self.redis.bgsave()
        print('done cards')

    def _write_record(self, card):
        """Write record from json to database.
        """
        self.redis.set(card.key, card.value)

    def _delete_by_pattern(self, pattern):
        """Delete all keys in given pattern.
        """
        matched_keys = []
        cur = 1
        while cur != 0:
            cur, keys = self.redis.scan(cur, pattern, 10000)
            matched_keys += keys
        if len(matched_keys) > 0:
            self.redis.delete(matched_keys)

    def init_db(self):
        """Initialize Redis database and load all cards.
        """
        self._delete_by_pattern('edition:*')
        self._delete_by_pattern('card:*')
        self._init_cards()
        self._init_sets()
        print('done init database')


class RedisSyncCollections():
    """Sync collections prices.
    """
    def __init__(self, host, port, db):
        self.redis = Redis(host=host, port=port, db=db)
