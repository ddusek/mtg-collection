import json
import requests
from mtg_collection import constants


class Downloader():
    """Download files needed for this application.
    """
    def _download_file(self, url, filename):
        """Download and write into a file.
        """
        with requests.get(url, stream=True) as response:
            # total_size_in_bytes = int(response.headers.get('content-length', 0))
            response.raise_for_status()

            with open(filename, 'wb') as json_file:
                for chunk in response.iter_content(chunk_size=1024000):
                    json_file.write(chunk)

    def download_scryfall_cards(self):
        """Fetch all cards bulk data from Scryfall.
        """
        response = requests.get(constants.SCRYFALL_BULK_URL)
        cards = json.loads(response.text)
        download_url = list(filter(lambda d: d['type'] == 'all_cards', cards['data']))[0]['download_uri']
        try:
            self._download_file(download_url, constants.SCRYFALL_CARDS_JSON_PATH)
            return True
        except Exception:
            return False
