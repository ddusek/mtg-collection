def scan_all(redis, text, limit=0):
    """Scan all keys in database and return keys with given text.

    :param redis: redis instance
    :param text: text to find in all keys
    :param limit: number of items to return (default (0) = all)
    :return: list of keys in bytes
    """
    text = text.lower()
    matched_keys = []
    cur = 1
    while cur != 0:
        cur, keys = redis.scan(cur, f'*{text}*', 10000)
        matched_keys += keys
        if len(matched_keys) >= limit > 0:
            return matched_keys[:limit]
    return matched_keys
