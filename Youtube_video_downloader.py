import yt_dlp
from datetime import datetime, timedelta
import os
import time
import random
import subprocess

def connect_vpn():
    try:
        subprocess.run(['sudo', 'protonvpn', 'c', '--fastest'], check=True)
        print("Connected to ProtonVPN using the fastest server")
    except subprocess.CalledProcessError as e:
        print(f"Failed to connect to ProtonVPN: {e}")

def disconnect_vpn():
    try:
        subprocess.run(['sudo', 'protonvpn', 'd'], check=True)
        print("Disconnected from ProtonVPN")
    except subprocess.CalledProcessError as e:
        print(f"Failed to disconnect ProtonVPN: {e}")

def download_recent_videos(channel_url, days=3, output_path='/media/alexm/ALEXM_HDD/DanielBaptist1611',
                           cookies_path='/path/to/your/cookies.txt'):
    ydl_opts = {
        'quiet': False,
        'format': 'bestvideo[height<=1080]+bestaudio/best',  # Try downloading 1080p or best available quality
        'merge_output_format': 'mp4',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'cookies': cookies_path,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
        }
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            playlist_dict = ydl.extract_info(channel_url, download=True)

            if 'entries' in playlist_dict:
                videos = playlist_dict['entries']
                print(f"Total videos found: {len(videos)}")

                date_threshold = datetime.now() - timedelta(days=days)

                for idx, video in enumerate(videos, start=1):
                    video_title = video.get('title', 'No title')
                    upload_date_str = video.get('upload_date', None)

                    if upload_date_str:
                        upload_date = datetime.strptime(upload_date_str, '%Y%m%d')

                        if upload_date >= date_threshold:
                            print(f"Downloading {idx}. {video_title} (Uploaded on: {upload_date.strftime('%Y-%m-%d')})")

                            # Connect to ProtonVPN before downloading
                            connect_vpn()

                            max_retries = 3
                            for attempt in range(max_retries):
                                try:
                                    ydl.download([video['webpage_url']])
                                    break
                                except Exception as e:
                                    print(f"Attempt {attempt + 1} failed: {e}")
                                    if attempt < max_retries - 1:
                                        sleep_time = random.uniform(10, 30)
                                        print(f"Retrying in {sleep_time:.2f} seconds...")
                                        time.sleep(sleep_time)
                                    else:
                                        print(f"Failed to download video after {max_retries} attempts. Skipping to next video.")

                            # Disconnect from ProtonVPN after downloading
                            disconnect_vpn()

                            sleep_time = random.uniform(10, 30)
                            print(f"Sleeping for {sleep_time:.2f} seconds before the next download...")
                            time.sleep(sleep_time)
                        else:
                            print(f"Skipping {idx}. {video_title} (Uploaded on: {upload_date.strftime('%Y-%m-%d')})")
            else:
                print("No videos found or unable to extract playlist.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    channel_url = 'https://www.youtube.com/@FortressBaptist/streams'
    output_folder = '/media/alexm/ALEXM_HDD/DanielBaptist1611'
    cookies_file_path = '/path/to/your/cookies.txt'  # Replace with the actual path to your cookies.txt file

    download_recent_videos(channel_url, days=12, output_path=output_folder, cookies_path=cookies_file_path)
