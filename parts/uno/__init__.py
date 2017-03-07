import json


def run(event, context):
    body = {
        'msg': 'hello world'
    }
    resp = {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps(body)
    }
    return resp
