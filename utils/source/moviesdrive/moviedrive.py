import requests
from bs4 import BeautifulSoup
import json
import asyncio
from playwright.async_api import async_playwright


class MoviesDrive:
    def __init__(self):
        self.base_url = 'https://moviesdrive.today/'
        
    def send_request(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def search(self, query):
        try:
            movies_list = []
            formatted_query = query.replace(" ", "+")
            search_url = f"{self.base_url}?s={formatted_query}"
            response = self.send_request(search_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                elements = soup.find_all(class_='thumb col-md-2 col-sm-4 col-xs-6')
                for element in elements:
                    a_tag = element.find('a')
                    href = a_tag.get('href', 'No href attribute') if a_tag else 'No <a> tag'
                    format_href = href.replace(self.base_url, '').replace('/', '')
                    img_tag = element.find('img')
                    if img_tag:
                        img_src = img_tag.get('src', 'No src attribute')
                        title = img_tag.get('title', 'No title attribute')
                        item_data = {
                            'title': title,
                            'image_source': img_src,
                            'id': format_href
                        }
                        movies_list.append(item_data)
            return movies_list
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_movies(self, page=1):
        try:
            movies_list = []
            if page > 1:
                url = f"{self.base_url}page/{page}/"
            else:
                url = self.base_url
            response = self.send_request(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                elements = soup.find_all(class_='thumb col-md-2 col-sm-4 col-xs-6')
                for element in elements:
                    a_tag = element.find('a')
                    href = a_tag.get('href', 'No href attribute') if a_tag else 'No <a> tag'
                    format_href = href.replace(self.base_url, '').replace('/', '')
                    img_tag = element.find('img')
                    if img_tag:
                        img_src = img_tag.get('src', 'No src attribute')
                        title = img_tag.get('title', 'No title attribute')
                        item_data = {
                            'title': title,
                            'image_source': img_src,
                            'id': format_href
                        }
                        movies_list.append(item_data)
            return movies_list
        except Exception as e:
            return {"success": False, "error": str(e)}
        
    def parse_movie(self, id):
        try:
            qualities_dict = {}
            url = f"{self.base_url}{id}/"
            response = self.send_request(url)            
            if response:
                soup = BeautifulSoup(response.content, 'html.parser')
                a_tags = soup.find_all('a', href=True)
                for a_tag in a_tags:
                    href = a_tag['href']
                    text = a_tag.get_text(strip=True)
                    if 'mdrive.social' in href:
                        qualities_dict[text] = href                    
            return qualities_dict
        except Exception as e:
            return {"success": False, "error": str(e)}
        
    def parse_tv_show(self, id):
        try:
            url = f"{self.base_url}{id}/"
            response = self.send_request(url)
            if response is None:
                return "Failed to retrieve data."
            soup = BeautifulSoup(response.content, 'html.parser')
            all_data = []
            h5_tags = soup.find_all('h5', style="text-align: center;")
            for h5 in h5_tags:
                red_span = h5.find('span', style="color: #ff0000;")
                if red_span:
                    season_text = red_span.get_text(strip=True)
                    blue_span = h5.find('span', style="color: #0000ff;")
                    if blue_span:
                        quality_text = blue_span.get_text(strip=True)
                        combined_text = f"{season_text} {quality_text}"
                        season_quality_dict = {}
                        next_a_tags = h5.find_all_next('a', href=True, limit=2) 
                        for a_tag in next_a_tags:
                            if 'mdrive.social' in a_tag['href']:
                                link_text = a_tag.get_text(strip=True)
                                link_href = a_tag['href']
                                season_quality_dict[link_text] = link_href
                        if season_quality_dict:
                            all_data.append({combined_text: season_quality_dict})
            return all_data
        except Exception as e:
            return {"success": False, "error": str(e)}
        
    def checker(self, id):
        if 'season' in id:
            return self.parse_tv_show(id)
        else:
            return self.parse_movie(id)
        
    def fetch_content_links(self, url):
        try:
            """Fetch content links from the given path."""
            response = self.send_request(url)
            if not response:
                return json.dumps({"error": "Failed to fetch URL content."}, indent=4)
            soup = BeautifulSoup(response.text, 'html.parser')
            content_data = {}
            episodes = soup.find_all('h5', style="text-align: center;")
            for ep in episodes:
                ep_text = ep.get_text(strip=True)
                if 'Ep' in ep_text:
                    ep_details = self.process_episodes(ep)
                    if ep_details: 
                        content_data[ep_text] = ep_details
            if not content_data:
                download_options = soup.find_all('h5', dir="auto", style="text-align: center;")
                for option in download_options:
                    link_text, link_url = self.process_download_options(option)
                    if link_url: 
                        content_data[link_text] = link_url
            return content_data
        except Exception as e:
            return {"success": False, "error": str(e)}
        
    def process_episodes(self, ep):
        """Extracts episode details."""
        ep_details = {}
        sibling = ep.find_next_sibling()
        while sibling and sibling.name == 'h5':
            link_text = sibling.get_text(strip=True)
            link_url = sibling.find('a')['href'] if sibling.find('a') else None
            if link_url and "HubCloud [Direct-DL]" not in link_text:
                ep_details[link_text] = link_url
            sibling = sibling.find_next_sibling()
        return ep_details

    def process_download_options(self, option):
        """Extracts download link text and URL."""
        if option.find('a'):
            link_text = option.get_text(strip=True)
            link_url = option.find('a')['href']
            if "HubCloud [Direct-DL]" not in link_text:
                return link_text, link_url
        return None, None

    async def scrape(self, id):
        try:
            furl = f"https://hubcloud.lol/video/{id}"
            playwright = await async_playwright().start()
            browser = await playwright.chromium.launch()
            page = await browser.new_page()
            await page.goto(furl)
            await page.wait_for_selector('a.btn.btn-primary', state='visible')
            first_button = await page.query_selector('a.btn.btn-primary')
            first_href = await first_button.get_attribute('href')
            await page.goto(first_href)
            await page.wait_for_selector('a.btn.btn-success.btn-lg.h6', state='visible', timeout=10000)
            second_button = await page.query_selector('a.btn.btn-success.btn-lg.h6')
            second_href = await second_button.get_attribute('href')
            await browser.close()
            await playwright.stop()
            return {"success": True, "stream": second_href}
        except Exception as e:
            if 'browser' in locals():
                await browser.close()
                await playwright.stop()
            return {"success": False, "error": str(e)}

    def run_scrape_sync(self, url):
        loop = asyncio.get_event_loop()
        if loop.is_running():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        result = loop.run_until_complete(self.scrape(url))
        loop.close()
        return result
    
'''#-------------------
# Example usage:
#-------------------
movies_drive = MoviesDrive()
# Example usage:

print(movies_drive.get_movies())  # Fetch movies from the first page
print(movies_drive.get_movies(page=2))  # Fetch movies from the second page

query = "tiger"  # Example search query
search_url = movies_drive.search(query)
print(search_url)

#MOVIE
quality_info = movies_drive.checker("ek-tha-tiger-2012")
print(quality_info)
#TVSHOW
quality_info = movies_drive.checker("crushed-season-1-4")
print(quality_info)
#MORE STREAMING LINKS
result = movies_drive.fetch_content_links("https://ww1.mdrive.social/archives/20193")
print(result)
#DIRECT STREAMING LINKS
print(movies_drive.run_scrape_sync('https://hubcloud.in/video/swxwdiq0fb435qb'))'''