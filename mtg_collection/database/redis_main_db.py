import sys
import json
from pathlib import Path
from redis import Redis
from .models import Card


class RedisMainSync():
    """Init or sync Redis database from json file.
    """
    def __init__(self, host, port, db):
        self.redis = Redis(host=host, port=port, db=db)
        self.lines = []
        self.lines_len = 0

    def __print_progress(self, i):
        if i % 1000 == 0:
            print(f'{format((i / self.lines_len * 100), ".2f")}% cards filled out of {self.lines_len} cards')
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
            key = f'{card_json["set_name"].lower()}:{card_json["name"].lower()}:{card_json["id"].upper()}'
            selected_value = {
                'name': card_json['name'],
                'set': card_json['set_name'],
                'price': card_json['prices']['usd'],
                'price_foil': card_json['prices']['usd_foil'],
                'release': card_json['released_at'],
                }
            value = json.dumps(selected_value)
            card_json = Card(key, value)
            return card_json
        except json.JSONDecodeError as err:
            print(err)
            return None
        except ValueError as err:
            print(err)
            return None

    def init_db(self):
        """Initialize Redis database and load all cards.
        """
        self._get_lines()
        self.redis.flushdb()
        for i, line in enumerate(self.lines):
            self.__print_progress(i)
            card = self._card_as_object(line)
            if card is None:
                continue
            self.write_card(card)
        self.redis.bgsave()
        print('done')

    def write_card(self, card):
        """Write card from json to database.
        """
        self.redis.set(card.key, card.value)


#  Redis structure
#  All cards
#   key, value
#   <collection>:<name>, <dictionary_values>
#  My cards
#   <custom_name(deck, whole_collection)>:<collection>:<name>, <dictinary_values>
