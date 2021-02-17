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
    cur = '0'
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


def get_set_keys(redis, set_name):
    """Get all keys in given set.
    """
    return redis.smembers(set_name)


def get_all_editions(redis):
    """Get all editions from database.
    """
    return get_set_keys(redis, 'editions')


def get_all_collections(redis):
    """Get all collections from database.
    """
    return get_set_keys(redis, 'collections')


def get_collection(redis, name):
    """Get all cards from collection.
    """
    print(name)
    keys = _get_matches(redis, f'collection:{name}:*')
    return redis.mget(keys)


def add_card_to_redis(redis, collection, card, units):
    """Add card and its units to a collection.
    """
    key = f'collection:{collection}:{card}:{units}'
    value = redis.get(card)
    return {'success': redis.set(key, value) if value else False}


def add_collection_to_redis(redis, collection):
    """Add new empty collection
    :return: 'success', 'failed' or 'exists' - if collection is already there.
    """
    if redis.get(f'collection:{collection}') is not None:
        return {'msg': 'exists'}
    redis.sadd('collections', collection)
    return {'success': True}


def format_cards(cards_data):
    """Format data from Redis to card objects.

    :param cards_data: Redis keys.
    """
    cards = []
    for i, data in enumerate(cards_data):
        data_list = data.split(':')
        card = ({'id': i, 'key': data, 'name': data_list[2], 'edition': data_list[1]})
        cards.append(card)
    return cards


def format_dropdown(data):
    """Format data from Redis objects to dropdown menu.

    :param data: Redis keys.
    """
    editions = []
    for i, data in enumerate(data):
        data_list = data.split(':')
        edition = ({'id': i, 'key': data, 'name': data_list[1]})
        editions.append(edition)
    return sorted(editions, key=lambda k: k['name'])


def format_set_dropdown(keys):
    """Format list of keys from Redis to dropdown menu.

    :param data: Redis keys list.
    """
    dropdown_data = []
    for i, data in enumerate(keys):
        dictionary = ({'id': i, 'key': data, 'name': data})
        dropdown_data.append(dictionary)
    return sorted(dropdown_data, key=lambda k: k['name'])
