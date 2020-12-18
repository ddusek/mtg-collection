def _order_by_name_key(text, cards):
    """Order cards by card name containing text, not edition.

    :param text: text to find in all keys
    :param cards: cards to order
    :return: ordered cards
    """
    prioritized = []
    rest = []
    for card in cards:
        card = card.decode('utf-8')
        name = card.split(':')[2]
        if text in name:
            prioritized.append(card)
        else:
            rest.append(card)
    matched = _full_match(text, prioritized)
    prioritized = [card for card in prioritized if card not in matched]
    return matched + prioritized + rest


def _full_match(text, cards):
    """Return list of cards where their name is match of the given text.
    """
    return [card for card in cards if card.split(':')[2] == text]


def _get_matches(redis, text):
    """Get keys from redis filtered by text.
    """
    matched_keys = []
    cur = 1
    while cur != 0:
        cur, keys = redis.scan(cur, text, 10000)
        matched_keys += keys
    return matched_keys


def get_suggestions(redis, text, limit=0):
    """Scan all keys in database and return keys with given text.

    :param redis: redis instance
    :param text: text to find in all keys
    :param limit: number of items to return (default (0) = all)

    :return: list of keys in bytes
    """
    text = text.lower()
    matches = _get_matches(redis, f'card:*{text}*')
    if len(matches) >= limit > 0:
        matches = _order_by_name_key(text, matches)
        return matches[:limit]
    return _order_by_name_key(text, matches)


def get_all_editions(redis):
    """Get all editions from database.
    """
    return _get_matches(redis, 'edition:*')


def get_collection(redis, name):
    """Get all cards from collection.
    """
    return _get_matches(redis, f'collection:{name}:*')


def get_collections(redis):
    """Get all collections
    """
    return _get_matches(redis, f'collection:*')
