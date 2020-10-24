class Card():
    """Model of card, used to save into Redis.
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value


class Parameters():
    def __init__(self, name, _set, price, price_foil, release):
        self.name = name
        self.set = _set
        self.price = price
        self.price_foil = price_foil
        self.release = release
