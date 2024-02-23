import requests

class VidSrcClient:
    def __init__(self, base_url="http://localhost:3001"):
        self.base_url = base_url

    def _send_request(self, endpoint):
        """Utility method to send requests to the server."""
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Received status code {response.status_code}")
            return None

    def get_vidsrc_source(self, db_id, season=None, episode=None):
        """Get video source for a TV show or movie. If it's a TV show, season and episode numbers can be provided."""
        if season is not None and episode is not None:
            endpoint = f"/vidsrc/{db_id}?s={season}&e={episode}"
        else:
            endpoint = f"/vidsrc/{db_id}"
        return self._send_request(endpoint)

    def get_vsrcme_source(self, db_id, season=None, episode=None):
        """Get video source for a TV show or movie. If it's a TV show, season and episode numbers can be provided."""
        if season is not None and episode is not None:
            endpoint = f"/vsrcme/{db_id}?s={season}&e={episode}"
        else:
            endpoint = f"/vsrcme/{db_id}"
        return self._send_request(endpoint)

    def get_subtitles(self, subtitle_url):
        """Fetch subtitles based on a provided URL."""
        # URL encode the subtitle_url parameter
        subtitle_url_encoded = requests.utils.quote(subtitle_url)
        endpoint = f"/subs/?url={subtitle_url_encoded}"
        return self._send_request(endpoint)

'''# Example usage
client = VidSrcClient()

# Get vidsrc source for a movie
print(client.get_vidsrc_source("297802"))

# Get vidsrc source for a TV show with season and episode
print(client.get_vidsrc_source("66732", season="1", episode="1"))

# Get vsrcme source for a movie
print(client.get_vsrcme_source("297802"))

# Get vsrcme source for a TV show with season and episode
print(client.get_vsrcme_source("66732", season="1", episode="1"))

# Get subtitles
#subtitle_url = "subtitle_url@opensubtitles.org"
#print(client.get_subtitles(subtitle_url))'''
