import random
import string


def key_generator(size: int = 16, chars: str = string.ascii_uppercase + string.ascii_lowercase + string.digits) -> str:
    """Generate random key.

    :param size: size of key, defaults to 16
    :type size: int, optional
    :param chars: allowed characters in key,
    defaults to string.ascii_uppercase+string.ascii_lowercase+string.digits
    :type chars: str, optional
    :return: generated key.
    :rtype: str
    """
    return ''.join(random.choice(chars) for _ in range(size))
