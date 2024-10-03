import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import yt_dlp

# YouTube channel URL (change this to your desired channel)
channel_url = 'https://www.youtube.com/c/YourChannel/videos'

# Threshold for number of days (set to 21)
days_threshold = 21
date_threshold = datetime.now() - timedelta(days=days_threshold)

print(f"Fetching YouTube channel page: {channel_url}")
response = requests.get(channel_url)

# Check if the page was fetched successfully
if response.status_code == 200:
    print("Page fetched successfully!")
else:
    print(f"Failed to fetch page. Status code: {response.status_code}")
    exit()

soup = BeautifulSoup(response.text, 'html.parser')

# List to store video URLs that meet the date threshold
video_urls = []

# Find all video elements (update the CSS selectors based on YouTube's HTML structure)
videos = soup.find_all('a', {'id': 'video-title'})

print(f"Found {len(videos)} videos on the page.")

for video in videos:
    video_url = 'https://www.youtube.com' + video['href']
    video_title = video['title']

    print(f"Processing video: {video_title}")

    # Find the corresponding upload date (this logic may vary depending on how YouTube renders the page)
    upload_date_element = video.find_next('div', {'id': 'metadata-line'})

    # If no upload date element is found, continue with the next video
    if upload_date_element is None:
        print(f"Could not find upload date for video: {video_title}")
        continue

    upload_date_text = upload_date_element.text.strip()

    print(f"Found upload date text: {upload_date_text}")

    # Simplified upload date processing (this logic assumes 'X days ago' format)
    if "days ago" in upload_date_text:
        try:
            days_ago = int(upload_date_text.split(' ')[0])
            upload_date = datetime.now() - timedelta(days=days_ago)

            # Check if the video was uploaded within the last 21 days
            if upload_date >= date_threshold:
                print(
                    f"Video {video_title} is within the last {days_threshold} days (uploaded {days_ago} days ago). Adding to download list.")
                video_urls.append(video_url)
            else:
                print(f"Video {video_title} is older than {days_threshold} days. Skipping.")
        except ValueError:
            print(f"Could not process upload date text: {upload_date_text}")
    else:
        print(f"Upload date does not match 'days ago' format. Skipping video: {video_title}")

print(f"Found {len(video_urls)} videos to download.")

# Feed video URLs to yt-dlp for downloading
for idx, video_url in enumerate(video_urls, start=1):
    print(f"Downloading video {idx}/{len(video_urls)}: {video_url}")
    with yt_dlp.YoutubeDL() as ydl:
        ydl.download([video_url])

print("Download process complete.")
