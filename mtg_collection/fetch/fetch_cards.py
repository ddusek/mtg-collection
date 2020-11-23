import json
from tqdm import tqdm
import requests


def download_file(url):
    """Download and write into a file.
    """
    with requests.get(url, stream=True) as response:
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        response.raise_for_status()

        with open('json_cards.json', 'wb') as json_file:
            for chunk in response.iter_content(chunk_size=1024000):
                progress_bar.update(len(chunk))
                json_file.write(chunk)
            progress_bar.close()


def fetch_bulk_cards():
    """Fetch all cards bulk data.
    """
    response = requests.get('https://api.scryfall.com/bulk-data')
    cards = json.loads(response.text)
    download_url = list(filter(lambda d: d['type'] == 'all_cards', cards['data']))[0]['download_uri']
    download_file(download_url)
