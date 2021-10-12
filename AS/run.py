import json
import socket
from datetime import datetime


# use python socket to start udp listening, and we can use json format.

# dns_query on port 53533


# listen to port 53533 to accept UDP connection, and store DNS record.

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1', 53533))
print('Bind UDP on 53533...')

while True:
    # 接收数据:
    data, addr = s.recvfrom(1024)
    print('Received from %s:%s.' % addr)
    data = json.loads(data)

    if data['method'] == 'query':
        key = data['name'] + ':' + data['type']
        with open('./registration_data.txt', 'r') as f:
            registration_data = f.read()
            registration_data = json.loads(registration_data)
            dns_data = registration_data.get(key)
            print(dns_data)
        dns_data['success'] = True
        s.sendto(json.dumps(dns_data).encode(), addr)

    if data['method'] == 'register':
        registration_data = {}
        with open('./registration_data.txt', 'r') as f:
            read = f.read()
            if read:
                registration_data = json.loads(read)

        key = data['name'] + ':' + data['type']
        registration_data[key] = data
        with open('./registration_data.txt', 'w') as f:
            f.write(json.dumps(registration_data, indent=4))

        res = json.dumps({'success': True})
        s.sendto(res.encode(), addr)

# s.sendto(b'Hello, %s!' % data, addr)

