import tweepy
import requests
import os

# Twitter API credentials
consumer_key = "your_consumer_key"
consumer_secret = "your_consumer_secret"
access_token = "your_access_token"
access_token_secret = "your_access_token_secret"

# FastAPI deepfake detection API URL
deepfake_api_url = "https://your-deployed-api-url/detect_deepfake/"

# Set up Tweepy authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if 'media' in status.entities:
            for media in status.entities['media']:
                if media['type'] == 'video':
                    video_url = media['media_url']
                    self.process_video(status.id, video_url)
        
    def process_video(self, tweet_id, video_url):
        try:
            # Download the video
            video_path = f"temp_{tweet_id}.mp4"
            response = requests.get(video_url, stream=True)
            if response.status_code == 200:
                with open(video_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)

                # Send the video to the deepfake detection API
                with open(video_path, 'rb') as video_file:
                    files = {'file': video_file}
                    api_response = requests.post(deepfake_api_url, files=files)
                    result = api_response.json()
                    print(f"Tweet ID: {tweet_id}, Result: {result}")


                os.remove(video_path)
            else:
                print(f"Failed to download video from URL: {video_url}")
        except Exception as e:
            print(f"Error processing video: {e}")

    def on_error(self, status_code):
        if status_code == 420:
            return False

stream_listener = MyStreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=['video'])
