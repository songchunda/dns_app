import json
import socket
from datetime import datetime

import requests
from flask import Flask, request
from flask import jsonify
app = Flask(__name__)


def success(data: dict=None) -> str:

    return jsonify(success=True, data=data)


def error(msg: str) -> str:

    return jsonify(success=False, data=msg)


@app.route('/')
def hello_world():
    return 'Hello world!'


@app.route('/time')
def current_time():
    fmt = '%Y-%m-%d %H:%M:%S'
    time = datetime.now().strftime(fmt)
    return time


@app.route('/fibonacci')
def fibonacci():
    hostname = request.args.get('hostname', '')
    fs_port = request.args.get('fs_port', '')
    number = request.args.get('number', '')
    as_ip = request.args.get('as_ip', '127.0.0.1')
    as_port = request.args.get('as_port', 53533, int)

    if not hostname:
        return error('hostname required')

    if not fs_port:
        return error('fs_port required')

    if not number:
        return error('number required')

    if not as_ip:
        return error('as_ip required')

    if not as_port:
        return error('as_port required')

    data = {
        'method': 'query',
        'name': hostname,
        'type': 'A',
    }

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    res = False
    r = {}
    while res is False:
        # 发送数据:
        s.sendto(json.dumps(data).encode(), (as_ip, as_port))
        # 接收数据:
        r = s.recv(1024).decode('utf-8')
        r = json.loads(r)
        print(r)
        res = r['success']

    url = 'http://' + r['value'] + ':' + fs_port
    url = url + '/fibonacci?number=' + number

    headers = {}
    headers['Content-Type'] = 'application/json'
    headers['Accept'] = 'application/json'

    resp = requests.get(url, headers=headers).json()

    return success(resp.get('data'))


app.run(host='0.0.0.0',
        port=8080,
        debug=True)
