import json


def run(event, context):
    body = {
        'msg': 'hello world'
    }
    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps(body)
    }
