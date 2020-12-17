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


def format_editions(editions_data):
    """Format data from Redis edition objects.

    :param editions_data: Redis keys.
    """
    editions = []
    for i, data in enumerate(editions_data):
        data_list = data.split(':')
        edition = ({'id': i, 'key': data, 'name': data_list[1]})
        editions.append(edition)
    return sorted(editions, key=lambda k: k['name'])
