def format_cards(cards_data):
    """Format data from Redis to card objects.

    :param cards_data: Redis keys.
    """
    cards = []
    for i, data in enumerate(cards_data):
        card = data.split(':')
        card = ({'id': i, 'key': data, 'name': card[2], 'edition': card[1]})
        cards.append(card)
    return cards


def format_editions(editions_data):
    """Format data from Redis edition objects.

    :param editions_data: Redis keys.
    """
    editions = []
    for i, data in enumerate(editions_data):
        edition = data.split(':')
        edition = ({'id': i, 'key': data, 'name': edition[1]})
        editions.append(edition)
    return editions
