class RedisObject():
    """Model of Redis object, used to save into database.
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
