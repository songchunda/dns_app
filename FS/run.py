import json
import socket
from datetime import datetime

from flask import Flask, request, Response
from flask import jsonify

app = Flask(__name__)


def success(data: dict=None) -> str:

    return jsonify(success=True, data=data)


def error(msg: str) -> str:

    return jsonify(success=False, data=msg)


@app.route('/')
def hello_world():
    return 'Hello world!'


@app.route('/register', methods=['PUT'])
def register():
    req = request.get_json(force=True)
    hostname = req.get('hostname', '')
    ip = req.get('ip', '127.0.0.1')
    as_ip = req.get('as_ip', '127.0.0.1')
    as_port = req.get('as_port', 53533)

    # send registration data to AS server using UDP
    data = {
        'method': 'register',
        'name': hostname,
        'value': ip,
        'type': 'A',
        'ttl': 3600,
    }

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    res = False

    while res is False:
        # 发送数据:
        s.sendto(json.dumps(data).encode(), (as_ip, as_port))
        # 接收数据:
        r = s.recv(1024).decode('utf-8')
        r = json.loads(r)
        print(r)
        res = r['success']

    s.close()

    return jsonify(success=True, code=201)


def get_fib_num(number):
    if number == 0:
        return 0
    a = 0
    b = 1
    while number > 0:
        a, b = b, a+b
        number -= 1
    print(b)
    return b


@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    number = request.args.get('number', 0, int)

    if not number:
        return Response(status=400)

    if not isinstance(number, int):
        return Response(status=400)

    fib_num = get_fib_num(number)

    return success(fib_num)


app.run(host='0.0.0.0',
        port=9090,
        debug=True)


# if __name__ == '__main__':
#     get_fib_num(1)
#     get_fib_num(2)
#     get_fib_num(3)
#     get_fib_num(4)
#     get_fib_num(5)
#     get_fib_num(6)
