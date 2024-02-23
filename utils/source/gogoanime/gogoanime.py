import requests

class GogoAnimeClient:
    def __init__(self, base_url="http://localhost:8787"):
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

    def search_anime(self, search_term):
        """Search for an anime by title."""
        search_term_encoded = requests.utils.quote(search_term)
        endpoint = f"/search/{search_term_encoded}"
        return self._send_request(endpoint)

    def get_anime_details(self, anime_id):
        """Get details of a specific anime."""
        endpoint = f"/anime/{anime_id}"
        return self._send_request(endpoint)

    def get_episode_stream_urls(self, episode_id):
        """Get episode stream URLs."""
        endpoint = f"/episode/{episode_id}"
        return self._send_request(endpoint)

    def get_episode_download_urls(self, episode_id):
        """Get episode download URLs."""
        endpoint = f"/download/{episode_id}"
        return self._send_request(endpoint)

    def get_home(self):
        """Get trending anime from Anilist and popular anime from GogoAnime."""
        endpoint = "/home"
        return self._send_request(endpoint)

'''# Example usage
client = GogoAnimeClient()

# Search for an anime
search_query = "Naruto"
print(client.search_anime(search_query))

# Get anime details
print(client.get_anime_details("naruto-dub"))

# Get episode stream URLs
print(client.get_episode_stream_urls("naruto-dub-episode-7"))

# Get episode download URLs
print(client.get_episode_download_urls("naruto-dub-episode-7"))

# Get trending and popular anime
print(client.get_home())'''
