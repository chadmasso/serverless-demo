# joins our path with the vendored folder so we
# have access to libraries
import os
import sys
here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, '../../vendored'))

import json
import settings

import twitter
from watson_developer_cloud import ToneAnalyzerV3
from slacker import Slacker


def send_slack(emotion):
    slack = Slacker(settings.SLACK_BOT_KEY)

    text = 'People mainly feel %s about chipotle' % emotion
    params = {
        'channel': '#serverless-demo',
        'text': text,
        'as_user': True,
    }
    slack.chat.post_message(**params)


def emotion_sort(a, b):
    if a['score'] > b['score']:
        return -1
    elif a['score'] < b['score']:
        return 1
    return 0


def run(event, context):
    q = '@ChipotleTweets'

    api = twitter.Api(
        consumer_key=settings.TWITTER_CONSUMER_KEY,
        consumer_secret=settings.TWITTER_CONSUMER_SECRET,
        access_token_key=settings.TWITTER_TOKEN,
        access_token_secret=settings.TWITTER_SECRET
    )

    statuses = api.GetSearch(term=q, count=100)
    status_texts = []
    for status in statuses:
        status_texts.append(status.text)

    tone_analyzer = ToneAnalyzerV3(
        username=settings.WATSON_USERNAME,
        password=settings.WATSON_PASSWORD,
        version='2016-05-19'
    )

    tones = tone_analyzer.tone(text=' '.join(status_texts), sentences=False, tones='emotion')
    emotion_tones = tones['document_tone']['tone_categories'][0]['tones']
    emotion_tones.sort(emotion_sort)

    main_emotion = emotion_tones[0]['tone_name']
    send_slack(main_emotion)
