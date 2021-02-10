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
