# joins our path with the vendored folder so we
# have access to libraries
import os
import sys
here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, '../../vendored'))

from settings import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_TOKEN, TWITTER_SECRET

import twitter
import json


def run(event, context):
    body = {
        'msg': 'hello world'
    }

    api = twitter.Api(
        consumer_key=TWITTER_CONSUMER_KEY,
        consumer_secret=TWITTER_CONSUMER_SECRET,
        access_token_key=TWITTER_TOKEN,
        access_token_secret=TWITTER_SECRET
    )

    statuses = api.GetSearch(term='#NationalPancakeDay', count=100)
    status_texts = []
    for status in statuses:
        status_texts.append(status.text)

    body = {
        'statuses': status_texts
    }
    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps(body)
    }
