import json
import os
import requests
from mtg_collection import constants
from mtg_collection.database import logger


class Synchronizer():
    """Init or synchronize Redis database from json file.
    """
    editions_url = constants.SCRYFALL_EDITIONS_URL

    def __init__(self, redis):
        self.redis = redis
        self.cards = []

    def _json_to_dict(self) -> None:
        """Get json file into python dict.
        """
        print('hello')
        try:
            with open(os.path.join(constants.ROOT_DIR, constants.SCRYFALL_CARDS_JSON_PATH), 'r') as file:
                self.cards = json.load(file)
        except OSError as err:
            logger.exception('cannot read json file with cards. %s. rootpath: %s, json_path: %s',
                             err, constants.ROOT_DIR, constants.SCRYFALL_CARDS_JSON_PATH)
        except TypeError as err:
            logger.exception(err)

    def _filter_card_fields(self, card: dict) -> dict:
        """Create card key and get only wanted card fields as value.

        :param card: Card object to get fields from.
        :type card: dict
        :return: New card object to be saved in database.
        :rtype: dict
        """
        card_edition = card["set_name"].lower().replace(":", ";")
        card_name = card["name"].lower().replace(":", ";")
        key = f'card:{card_edition}:{card_name}'
        values = {
            'name': card['name'],
            'edition': card['set_name'],
            'price': card['prices']['usd'],
            'price_foil': card['prices']['usd_foil'],
            'release': card['released_at'],
        }
        return {'key': key, 'value': values}

    def _filter_edition_fields(self, edition: dict) -> dict:
        """Create edition key and get only wanted edition fields as value.

        :param edition: Edition object to get fields from.
        :type edition: dict
        :return: new Edition object to be saved in database.
        :rtype: dict
        """
        # replace ':' because its used as key parts separator in Redis.
        key = f'edition:{edition["name"].lower().replace(":", ";")}'
        values = {
            'image': edition['icon_svg_uri'],
            'name': edition['name'],
            'released': edition['released_at']
        }
        return ({'key': key, 'value': values})

    def _init_editions(self) -> None:
        """Save all editions in database.
        """
        response = requests.get(self.editions_url)
        editions = response.json()
        for edition in editions['data']:
            if edition is not None:
                self._write_record(self._filter_edition_fields(edition), 'editions')
        self.redis.bgsave()

    def _init_cards(self) -> None:
        """Save all cards in database.
        """
        self._json_to_dict()
        for card in self.cards:
            if card is not None:
                self._write_record(self._filter_card_fields(card), 'card')
        self.redis.bgsave()

    def _write_record(self, obj: dict, set_name: str = None) -> None:
        """Write record from json to database.

        :param obj: obj to write.
        :type obj: dict
        :param set_name: if not None, add obj['key'] to this set. Defaults to None
        :type set_name: str, optional
        """
        self.redis.set(obj['key'], json.dumps(obj['value']))
        if set_name is not None:
            self.redis.sadd(set_name, obj['key'])

    def _delete_by_pattern(self, pattern: str) -> None:
        """Delete all keys in given pattern.

        :param pattern: pattern to match keys from.
        :type pattern: str
        """
        matched_keys = self.redis.scan_iter(pattern, 10000)
        for key in matched_keys:
            self.redis.delete(key)

    def synchronize_database(self) -> bool:
        """Synchronize cards and editions in database with a file.

        :return: True if success.
        :rtype: bool
        """
        try:
            self._delete_by_pattern('edition:*')
            self._delete_by_pattern('card:*')
            self._init_cards()
            self._init_editions()
            return True
        except (ConnectionError, TimeoutError) as err:
            logger.exception(err)
