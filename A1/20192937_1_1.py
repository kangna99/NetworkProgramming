"""
[3 points] Write a Python script for demonstrating "Raw Network Conversation."
Use socket library to request Open Notify API to GET an estimate for when the ISS will fly over a specified point.

parameters = {'lat':'45', 'lon':'180'}
base_address = http://api.open-notify.org/iss-pass.json
"""
import socket

request_text = """\
GET /iss-pass.json?lat={}&lon={}&format=json HTTP/1.1\r\n\
Host: api.open-notify.org\r\n\
User-Agent: nayoon\r\n\
Connection: close\r\n\
\r\n\
"""


def geocode(lat, lon):
    sock = socket.socket()
    sock.connect(('api.open-notify.org', 80))
    request = request_text.format(lat, lon)
    print(request)
    sock.sendall(request.encode('ascii'))
    raw_reply = b''  # generate text as byte type
    while True:
        more = sock.recv(4096)
        if not more:
            break
        raw_reply += more
    print(raw_reply.decode('utf-8'))


if __name__ == '__main__':
    geocode(45, 180)
