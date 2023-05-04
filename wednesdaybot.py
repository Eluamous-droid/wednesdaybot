import os
import discord
import random
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
playlist_id = 'PLy3-VH7qrUZ5IVq_lISnoccVIYZCMvi-8'
YOUTUBE_TOKEN = os.getenv('YOUTUBE_TOKEN')


def get_videos_in_playlist(playlist_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    videos = []
    next_page_token = ''
    while next_page_token is not None:
        res = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()
        videos += res['items']
        next_page_token = res.get('nextPageToken')
    return videos

videos = get_videos_in_playlist(playlist_id, YOUTUBE_TOKEN)
random_video = random.choice(videos)
video_url = 'https://www.youtube.com/watch?v=' + random_video['snippet']['resourceId']['videoId']


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    channel = client.get_channel(456526207136169987)
    await channel.send('Its wednesday my dudes \n'+video_url)
    await client.close()



client.run(DISCORD_TOKEN)