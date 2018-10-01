import base64
import tempfile
import requests
import urllib.parse

from carball.decompile_replays import analyze_replay_file
try:
    import config
    API_KEY = config.API_KEY
except:
    print('No config file, anyone can access the function!')
    API_KEY = None

def decompile_replay(filename):
    proto_manager = analyze_replay_file(filename, filename + '.json')
    _, proto_name = tempfile.mkstemp()
    with open(proto_name, 'wb') as f:
        proto_manager.write_proto_out_to_file(f)
    _, pandas_name = tempfile.mkstemp()
    with open(pandas_name, 'wb') as f:
        proto_manager.write_pandas_out_to_file(f)
    return proto_name, pandas_name


def write_file(decoded):
    _, name = tempfile.mkstemp()
    with open(name, 'wb') as f:
        f.write(decoded)
    return name


def parse_replay(request):
    from flask import jsonify
    if API_KEY is not None:
        if 'key' in request.args:
            if request.args['key'] != API_KEY:
                return jsonify({'status': 'Invalid API key.'}), 401
        else:
            return jsonify({'status': 'No API key supplied.'}), 401
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <http://flask.pocoo.org/docs/0.12/api/#flask.Request>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <http://flask.pocoo.org/docs/0.12/api/#flask.Flask.make_response>.
    """
    decoded_file = base64.b64decode(request.data)
    name = write_file(decoded_file)

    proto, pandas = decompile_replay(name)
    with open(proto, 'rb') as f:
        encoded_proto = base64.b64encode(f.read()).decode()
    with open(pandas, 'rb') as f:
        encoded_pandas = base64.b64encode(f.read()).decode()

    obj = {
        'status': '200',
        'proto': encoded_proto,
        'pandas': encoded_pandas
    }

    if 'webhook' in request.args:
        r = requests.post(urllib.parse.unquote(request.args['webhook']), json=obj)
    return jsonify(obj)
