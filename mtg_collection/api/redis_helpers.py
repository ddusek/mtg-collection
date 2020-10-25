def scan_all(redis, text):
    """Scan all keys in database and return keys with given text.

    :param redis: redis instance
    :param text: text to find in all keys
    :return: list of keys in bytes
    """
    matched_keys = []
    cur, keys = redis.scan(0, f'*{text}*', 10000)
    matched_keys += keys

    while cur != 0:
        cur, keys = redis.scan(cur, f'*{text}*', 10000)
        matched_keys += keys
    return matched_keys
