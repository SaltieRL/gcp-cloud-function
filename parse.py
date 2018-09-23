import base64
import io
import json

from carball.decompile_replays import analyze_replay_file


def decompile_replay(filename):
    proto_manager = analyze_replay_file(filename, filename + '.json')
    proto = io.BytesIO()
    proto_manager.write_proto_out_to_file(proto)
    pandas = io.BytesIO()
    proto_manager.write_pandas_out_to_file(pandas)
    return proto, pandas


def write_file(decoded, filename):
    with open(filename, 'wb') as f:
        f.write(decoded)
    return True


def lambda_handler(event, context):
    # TODO implement
    decoded_file = base64.b64decode(event['body']['file'])

    encoded_string = base64.b64encode(image_file.read())

    obj = {
        'status': '200',
        'event': event
    }
    return {
        "statusCode": 200,
        "body": json.dumps(obj)
    }
