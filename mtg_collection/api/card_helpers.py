def format_cards(cards_data):
    """Format data from Redis to card objects.

    :param cards_data: Redis keys.
    """
    cards = []
    for i, data in enumerate(cards_data):
        edition_name = data.split(':')
        card = ({'id': i, 'key': data, 'name': edition_name[1], 'edition': edition_name[0]})
        cards.append(card)
    return cards
