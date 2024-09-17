import os
import googleapiclient.discovery


# Function to get all videos from a YouTube channel
def get_channel_videos(api_key, channel_id):
    # Disable OAuthlib's HTTPS verification when running locally
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # Initialize YouTube API client
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    # List to store video details
    video_list = []

    # Request to get uploads playlist id for the channel
    request = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    )
    response = request.execute()

    # Get the uploads playlist ID (each channel has one)
    uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    # Paginate through all videos in the playlist
    next_page_token = None
    while True:
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=uploads_playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        # Extract video details
        for item in response['items']:
            video_info = {
                'videoId': item['snippet']['resourceId']['videoId'],
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'publishedAt': item['snippet']['publishedAt']
            }
            video_list.append(video_info)

        # Check if there is another page
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return video_list


# Usage
if __name__ == "__main__":
    API_KEY = 'YOUR_API_KEY'  # Replace with your YouTube Data API key
    CHANNEL_ID = 'UC_x5XG1OV2P6uZZ5FSM9Ttw'  # Replace with the YouTube channel ID

    videos = get_channel_videos(API_KEY, CHANNEL_ID)

    # Print video metadata
    for video in videos:
        print(f"Video ID: {video['videoId']}")
        print(f"Title: {video['title']}")
        print(f"Description: {video['description']}")
        print(f"Published at: {video['publishedAt']}\n")
