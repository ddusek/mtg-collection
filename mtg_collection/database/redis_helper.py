import json
from mtg_collection.database import logger


def _order_by_name_key(text: str, cards: list[bytes]) -> list[str]:
    """Order cards by full match, card containing text and not edition, then rest.

    :param text: Text to find in all keys.
    :type text: str
    :param cards: Cards to order.
    :type cards: str
    :return: Ordered cards.
    :rtype: list[str]
    """
    prioritized = []
    rest = []
    for card_bytes in cards:
        card = card_bytes.decode("utf-8")
        card_fields = card.split(":")
        if len(card_fields) < 3:
            raise IndexError("card key format is invalid", card_bytes)
        name = card_fields[2]
        if text in name:
            prioritized.append(card)
        else:
            rest.append(card)
    matched = _full_match(text, prioritized)
    prioritized = [card for card in prioritized if card not in matched]
    return matched + prioritized + rest


def _full_match(name: str, cards: list) -> list[str]:
    """Return list of cards where their name is match of the given text.

    :param name: Name of card to find.
    :type name: str
    :param cards: List of cards where to find match.
    :type cards: list
    :return: List of matched cards.
    :rtype: list[str]
    """
    return [card for card in cards if card.split(":")[2] == name]


def _get_matches(redis: "Redis", text: str) -> list[str]:
    """Get keys from redis filtered by text.

    :param redis: Redis instance.
    :type redis: Redis
    :param text: Text to find in keys.
    :type text: str
    :return: List of matched keys.
    :rtype: list[str]
    """
    matched_keys = []
    cur = "0"
    while cur != 0:
        cur, keys = redis.scan(cur, text, 10000)
        matched_keys += keys
    return matched_keys


def get_suggestions(redis: "Redis", text: str, limit: int = 0) -> list[str]:
    """Scan all keys in database and return keys with given text.


    :return: list of keys in bytes

    :param redis: Redis instance.
    :type redis: Redis
    :param text: Text to find in all keys.
    :type text: str
    :param limit: Number of items to return (default (0) = all).
    :type limit: int, optional
    :return: List of keys.
    :rtype: list[str]
    """
    if text is None:
        logger.warning("suggest text should not be empty")
    text = text.lower()
    matches = _get_matches(redis, f"card:*{text}*")
    if len(matches) >= limit > 0:
        try:
            matches = _order_by_name_key(text, matches)
            return matches[:limit]
        except IndexError as err:
            logger.exception(err)
    try:
        return _order_by_name_key(text, matches)
    except IndexError as err:
        logger.exception(err)


def get_set_keys(redis: "Redis", set_name: str, prefix: str = None) -> list[str]:
    """Get all keys in given set.

    :param redis: Redis instance.
    :type redis: Redis
    :param set_name: Name of set.
    :type set_name: str
    :param prefix: Prefix by which to filter keys.
    :type prefix: str
    :return: List of keys.
    :rtype: list[str]
    """
    prefix_bytes = f"{prefix}:".encode()
    keys = redis.smembers(set_name)
    print(keys)
    if prefix:
        keys = [k.removeprefix(prefix_bytes) for k in keys if prefix_bytes in k]
    return keys


def get_all_editions(redis: "Redis") -> list[str]:
    """Get all editions from database.

    :param redis: Redis instance.
    :type redis: Redis
    :return: List of keys.
    :rtype: list[str]
    """
    return get_set_keys(redis, "editions")


def get_all_collections(redis: "Redis", user: str) -> list[str]:
    """Get all collections from database.

    :param redis: Redis instance.
    :type redis: Redis
    :param user: Username of user whose collections to get.
    :type user: str
    :return: List of keys.
    :rtype: list[str]
    """
    return get_set_keys(redis, "collections", user)


def get_collection(redis: "Redis", name: str) -> list[str]:
    """Get all cards from collection.

    :param redis: Redis instance.
    :type redis: Redis
    :param name: Name of collection.
    :type name: str
    :return: List of keys.
    :rtype: list[str]
    """
    keys = _get_matches(redis, f"collection:{name}:*")
    return redis.mget(keys)


def add_card_to_redis(
    redis: "Redis", user: str, collection: str, card: str, edition: str, units: int
) -> object:
    """Add card and to a collection.

    :param redis: Redis instance.
    :type redis: Redis
    :param user: User to whom to add card.
    :type user: str
    :param collection: Collection where to add card.
    :type collection: str
    :param card: Card to add.
    :type card: str
    :param edition: Edition of card to add.
    :type edition: str
    :param units: Number of units to add.
    :type units: int
    :return: {"success": bool}
    :rtype: object
    """
    if not user:
        raise ValueError("cannot add card, user part is None")
    if not collection:
        raise ValueError("cannot add card, collection part is None")
    if not card:
        raise ValueError("cannot add card, card part is None")
    if not units:
        raise ValueError("cannot add card, units part is None")
    key = f"collection:{user}:{collection}:{card}"
    matched = _get_matches(redis, key)
    if len(matched) > 0:
        return {"success": False, "message": "Card already exists."}

    value = redis.get(f"card:{edition}:{card}")
    value_dict = json.loads(value.decode("utf-8"))
    value_dict["units"] = units
    print(value_dict)
    value = str.encode(json.dumps(value_dict), "utf-8")
    if value is None:
        raise ValueError(
            "cannot add card, its value was not found by card key",
            card,
            f"card:{edition}:{card}",
        )
    return {"success": redis.set(key, value) if value else False}


def add_collection_to_redis(redis: "Redis", collection: str, user: str) -> object:
    """Add new empty collection.

    If collection is already in set, it gets rewritten so basically nothing happens.

    :param redis: Redis instance.
    :type redis: Redis
    :param collection: Name of collection.
    :type collection: str
    :param user: Username.
    :type user: str
    :return: {"success": bool}.
    :rtype: object
    """
    return {"success": redis.sadd("collections", f"{user}:{collection}")}


def format_cards(cards_data: list[str]) -> list[str]:
    """Format data from Redis to card objects.

    :param cards_data: Redis keys.
    :type cards_data: list[str]
    :return: List of cards.
    :rtype: list[str]
    """
    cards = []
    for i, data in enumerate(cards_data):
        data_list = data.split(":")
        if len(data_list) < 3:
            raise IndexError("card is in wrong format", cards_data)
        card = {"id": i, "key": data, "name": data_list[2], "edition": data_list[1]}
        cards.append(card)
    return cards


def format_dropdown(keys: list[str]) -> list[dict]:
    """Format keys from Redis objects to dropdown menu.

    :param keys: Redis keys, where key[0] will be used as dict value for name.
    :type keys: list[str]
    :return: List of items ready for dropdown menu.
    :rtype: list[dict]
    """
    editions = []
    for i, data in enumerate(keys):
        edition = {"id": i, "key": data, "name": data}
        editions.append(edition)
    return sorted(editions, key=lambda k: k["name"])


def format_set_dropdown(keys: list[str]) -> list[dict]:
    """Format data from Redis objects to dropdown menu.

    :param keys: Redis keys list.
    :type keys: list[str]
    :return: List of items ready for dropdown menu.
    :rtype: list[dict]
    """
    dropdown_data = []
    for i, data in enumerate(keys):
        dictionary = {"id": i, "key": data, "name": data}
        dropdown_data.append(dictionary)
    return sorted(dropdown_data, key=lambda k: k["name"])
