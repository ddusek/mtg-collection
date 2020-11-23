def scan_all(redis, text, limit=0, order_by=''):
    """Scan all keys in database and return keys with given text.

    :param redis: redis instance
    :param text: text to find in all keys
    :param limit: number of items to return (default (0) = all)
    :param order_by: determine which parameter of matched cards should be displayed first
    (name - first show all cards where name contains given text then all editions,
    edition - same but reverted,
    empty - dont order items)

    :return: list of keys in bytes
    """
    text = text.lower()
    matched_keys = []
    cur = 1
    while cur != 0:
        cur, keys = redis.scan(cur, f'*{text}*', 10000)
        matched_keys += keys
        if len(matched_keys) >= limit > 0:
            ordered = order_items(text, matched_keys[:limit*5], order_by)
            return ordered[:limit]
    return order_items(text, matched_keys, order_by)


def order_items(text, cards, order_by):
    """Order cards by name or edition.

    :param text: text to find in all keys
    :param cards: cards to order
    :param order_by: 'name' or 'edition'
    :return: ordered cards
    """
    prioritized = []
    rest = []
    if order_by == 'name':
        for card in cards:
            card = card.decode('utf-8')
            if ':' in card:
                edition, name = card.split(':')
                if text in name:
                    prioritized.append(card)
                else:
                    rest.append(card)
        return prioritized + rest

    if order_by == 'edition':
        for card in cards:
            card = card.decode('utf-8')
            if text in edition:
                prioritized.append(card)
            else:
                rest.append(card)
        return prioritized + rest
    return cards
