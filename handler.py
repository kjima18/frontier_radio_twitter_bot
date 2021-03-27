from apiclient.discovery import build
from apiclient.errors import HttpError
import tweepy
import random
import os

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
searches = []

youtube = build(
  YOUTUBE_API_SERVICE_NAME,
  YOUTUBE_API_VERSION,
  developerKey=os.environ['YOUTUBE_API_KEY']
)

nextPagetoken = None
nextPagetokenParam = None

while True:
  if nextPagetoken != None:
    nextPagetokenParam = nextPagetoken

  search_response = youtube.search().list(
    part = 'snippet',
    channelId = os.environ['FRONTIER_RADIO_CHANNEL_ID'],
    pageToken = nextPagetokenParam
  ).execute()

  for search_result in search_response.get('items', []):
    if search_result['id']['kind'] == 'youtube#video':
      searches.append([
        f'https://www.youtube.com/watch?v={search_result["id"]["videoId"]}',
        search_result['snippet']['title']
      ])

  try:
    nextPagetoken = search_response['nextPageToken']
  except:
      break

def tweet(event, context):
  target_video = random.choice(searches)
  tweet_text = f'''
  {target_video[1]}
  {target_video[0]}

  #フロンティアラジオ #建築 #まちづくり #HEAD研究会
  '''

  auth = tweepy.OAuthHandler(os.environ['TW_CONSUMER_KEY'], os.environ['TW_CONSUMER_SECRET'])
  auth.set_access_token(os.environ['TW_ACCESS_TOKEN'], os.environ['TW_ACCESS_TOKEN_SECRET'])
  api = tweepy.API(auth)
  api.update_status(tweet_text)
