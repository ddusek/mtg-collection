import sys
# from database.redis_collections_db import RedisCollections
from database.redis_main_db import RedisMainSync
from fetch.fetch_cards import fetch_bulk_cards

if __name__ == '__main__':
    PARAMC = '\033[96m'
    YELLOWC = '\33[33m'
    ENDC = '\033[0m'
    if len(sys.argv) < 2:
        print(f'{YELLOWC}No arguments passed. Type help as first parameter for available arguments.{ENDC}')
    elif sys.argv[1] == 'help':
        print(f'''{YELLOWC}available parameters{ENDC}:
    {PARAMC}initdb{ENDC}: delete and initialize new main database with all cards
    {PARAMC}fetchcards{ENDC}: download json file with all cards.
        ''')
    elif sys.argv[1] == 'initdb':
        sync = RedisMainSync(host='0.0.0.0', port=6379, db=0)
        sync.init_db()
    elif sys.argv[1] == 'fetchcards':
        fetch_bulk_cards()
