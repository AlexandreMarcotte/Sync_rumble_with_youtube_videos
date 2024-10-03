import yt_dlp
from datetime import datetime, timedelta
import os
import time
import random
import subprocess
import copy


class YouTubeVideoDownloader:
    def __init__(self, channel_url, output_path, cookies_path, vpn=True, max_videos=1, max_metadata=5):
        """
        Initializes the downloader with the channel URL, output path, cookies path, VPN flag,
        maximum number of videos to download, and maximum number of metadata entries to fetch.

        :param channel_url: URL of the YouTube channel
        :param output_path: Path where videos will be downloaded
        :param cookies_path: Path to the cookies file
        :param vpn: Boolean indicating whether to use VPN (default: True)
        :param max_videos: Limit on how many videos to download
        :param max_metadata: Limit on how many metadata entries to extract
        """
        self.channel_url = channel_url
        self.output_path = output_path
        self.cookies_path = cookies_path
        self.vpn = vpn
        self.max_videos = max_videos  # Limit the number of videos to download
        self.max_metadata = max_metadata  # Limit the number of metadata entries to fetch

        self.base_ydl_opts = {
            'quiet': False,
            'format': 'bestvideo[height<=1080]+bestaudio/best',  # Download 1080p or best available quality
            'merge_output_format': 'mp4',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'cookies': cookies_path,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/92.0.4515.159 Safari/537.36'
            },
            'playlist_end': max_metadata  # Limit metadata extraction
        }

    def connect_vpn(self):
        """Connects to the fastest ProtonVPN server."""
        if self.vpn:
            try:
                subprocess.run(['sudo', 'protonvpn', 'c', '--fastest'], check=True)
                print("Connected to ProtonVPN using the fastest server")
            except subprocess.CalledProcessError as e:
                print(f"Failed to connect to ProtonVPN: {e}")

    def disconnect_vpn(self):
        """Disconnects from ProtonVPN."""
        if self.vpn:
            try:
                subprocess.run(['sudo', 'protonvpn', 'd'], check=True)
                print("Disconnected from ProtonVPN")
            except subprocess.CalledProcessError as e:
                print(f"Failed to disconnect from ProtonVPN: {e}")

    def download_video(self, video_url):
        """Downloads a single video with retry mechanism."""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                with yt_dlp.YoutubeDL(self.base_ydl_opts) as ydl:
                    ydl.download([video_url])
                print(f"Successfully downloaded: {video_url}")
                break  # Exit loop on success
            except Exception as e:
                print(f"Attempt {attempt + 1} failed for {video_url}: {e}")
                if attempt < max_retries - 1:
                    sleep_time = random.uniform(10, 30)
                    print(f"Retrying in {sleep_time:.2f} seconds...")
                    time.sleep(sleep_time)
                else:
                    print(f"Failed to download {video_url} after {max_retries} attempts. Skipping.")

    def get_updated_ydl_opts(self, date_threshold_str):
        """
        Generates updated yt_dlp options with date filtering.

        :param date_threshold_str: Date string in 'YYYYMMDD' format
        :return: Updated yt_dlp options dictionary
        """
        updated_opts = copy.deepcopy(self.base_ydl_opts)
        updated_opts['dateafter'] = date_threshold_str  # Only fetch videos after this date
        return updated_opts

    def download_recent_videos(self, days):
        """
        Downloads videos uploaded within the last 'days' days, limited by max_videos and max_metadata.

        :param days: Number of days to look back from the current date
        """
        print(f"Preparing to download videos from the last {days} days...")

        date_threshold = datetime.now() - timedelta(days=days)
        date_threshold_str = date_threshold.strftime('%Y%m%d')
        videos_to_download = []

        # Generate yt_dlp options with date filtering
        ydl_opts = self.get_updated_ydl_opts(date_threshold_str)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                # Extract information about the channel with date and metadata limits
                print("Extracting video metadata...")
                playlist_dict = ydl.extract_info(self.channel_url, download=False)

                if 'entries' not in playlist_dict:
                    print("No videos found or unable to extract playlist.")
                    return

                print(f"Total metadata entries fetched: {len(playlist_dict['entries'])}")

                for idx, video in enumerate(playlist_dict['entries'], start=1):
                    video_title = video.get('title', 'No title')
                    upload_date_str = video.get('upload_date', None)

                    if not upload_date_str:
                        print(f"Video '{video_title}' has no upload date. Skipping.")
                        continue

                    upload_date = datetime.strptime(upload_date_str, '%Y%m%d')

                    if upload_date < date_threshold:
                        print(f"Video '{video_title}' is older than {days} days. Skipping.")
                        continue

                    video_url = video.get('webpage_url', None)
                    if not video_url:
                        print(f"Video '{video_title}' has no URL. Skipping.")
                        continue

                    print(
                        f"Queued for download: {idx}. {video_title} (Uploaded on: {upload_date.strftime('%Y-%m-%d')})")
                    videos_to_download.append(video_url)

                    if len(videos_to_download) >= self.max_videos:
                        print(f"Reached the download limit of {self.max_videos} videos.")
                        break

                if not videos_to_download:
                    print("No videos to download based on the given criteria.")
                    return

                print(f"Starting download of {len(videos_to_download)} videos...")

                for idx, video_url in enumerate(videos_to_download, start=1):
                    print(f"\nDownloading video {idx}/{len(videos_to_download)}: {video_url}")

                    self.connect_vpn()
                    self.download_video(video_url)
                    self.disconnect_vpn()

                    if idx < len(videos_to_download):
                        sleep_time = random.uniform(10, 30)
                        print(f"Sleeping for {sleep_time:.2f} seconds before the next download...")
                        time.sleep(sleep_time)

                print("All downloads completed.")

            except Exception as e:
                print(f"An error occurred while extracting metadata: {str(e)}")


# Example usage
if __name__ == "__main__":
    channel_url = 'https://www.youtube.com/@FortressBaptist/streams'
    output_folder = '/media/alexm/ALEXM_HDD/FortressBaptist'
    cookies_file_path = '/path/to/your/cookies.txt'  # Replace with the actual path to your cookies.txt file

    # Initialize the downloader with a limit of 2 videos and 50 metadata entries
    downloader = YouTubeVideoDownloader(
        channel_url=channel_url,
        output_path=output_folder,
        cookies_path=cookies_file_path,
        vpn=True,
        max_videos=2,  # Limit on number of videos to download
        max_metadata=4  # Limit on number of metadata entries to fetch
    )

    # To download videos from the last 12 days
    days = 12  # Number of days to filter

    downloader.download_recent_videos(days)
