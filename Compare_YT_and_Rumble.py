import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup


class RumbleScraper:
    def __init__(self, base_url, max_pages=10):
        self.base_url = base_url
        self.max_pages = max_pages
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        self.session = self._configure_session()

    def _configure_session(self):
        """Configures an HTTP session with retry strategy."""
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"],
            backoff_factor=1
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session = requests.Session()
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        return session

    def scrape_titles(self):
        """Scrapes video titles from multiple pages and returns them as a list."""
        all_titles = []
        for page_num in range(1, self.max_pages + 1):
            try:
                url = f"{self.base_url}{page_num}"
                response = self.session.get(url, headers=self.headers, timeout=10)

                if response.status_code != 200:
                    print(f"Page {page_num} not found or failed to load.")
                    break

                soup = BeautifulSoup(response.content, 'html.parser')
                titles = soup.find_all('h3', class_='thumbnail__title')

                if not titles:
                    print(f"No more titles found on page {page_num}. Stopping.")
                    break

                for title in titles:
                    all_titles.append(title.get_text(strip=True))

            except requests.exceptions.RequestException as e:
                print(f"Error encountered on page {page_num}: {e}")
                break

        return all_titles

    def get_local_videos(self, folder_path):
        """Retrieves the list of video file names from the specified local folder."""
        try:
            # List all files in the directory
            video_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
            return video_files
        except Exception as e:
            print(f"Error reading the folder {folder_path}: {e}")
            return []

    def compare_videos(self, rumble_titles, local_videos):
        """Compares Rumble video titles to the list of local video files and finds videos not uploaded yet."""
        not_uploaded = []

        # Clean up local video file names (remove extensions, etc.) for comparison
        local_videos_cleaned = [os.path.splitext(video)[0] for video in local_videos]

        # Compare each Rumble title with local video names
        for title in rumble_titles:
            if title not in local_videos_cleaned:
                not_uploaded.append(title)

        return not_uploaded


# Example usage:
if __name__ == "__main__":
    # Instantiate the scraper class
    base_url = "https://rumble.com/user/FortressBaptist?page="
    scraper = RumbleScraper(base_url, max_pages=10)

    # Call the scrape_titles method to get the list of Rumble videos
    rumble_titles = scraper.scrape_titles()

    # Get the list of local videos from the folder
    folder_path = "/media/alexm/ALEXM_HDD/uploaded_video"
    local_videos = scraper.get_local_videos(folder_path)

    # Compare and find videos not uploaded yet
    not_uploaded_videos = scraper.compare_videos(rumble_titles, local_videos)

    # Print the list of videos not uploaded yet
    if not_uploaded_videos:
        print("Videos not uploaded yet:")
        for video in not_uploaded_videos:
            print(video)
    else:
        print("All videos have been uploaded.")
