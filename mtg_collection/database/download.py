import json
# from tqdm import tqdm
import requests
import constants


def _download_file(url):
    """Download and write into a file.
    """
    with requests.get(url, stream=True) as response:
        # total_size_in_bytes = int(response.headers.get('content-length', 0))
        response.raise_for_status()

        with open(constants.SCRYFALL_CARDS_JSON_PATH, 'wb') as json_file:
            for chunk in response.iter_content(chunk_size=1024000):
                json_file.write(chunk)


def fetch_bulk_cards():
    """Fetch all cards bulk data.
    """
    response = requests.get(constants.SCRYFALL_BULK_URL)
    cards = json.loads(response.text)
    download_url = list(filter(lambda d: d['type'] == 'all_cards', cards['data']))[0]['download_uri']
    _download_file(download_url)


fetch_bulk_cards()
