"""
2. [3 points] Write a python script to create a UDP Server and Client using python socket standard library.

The server can check the received data size:
 if the received data size is even in number,
           reply with received data size,
 else
       reply with "Error 403 Forbidden."

Example:
Suppose the client sent "Soongsil University" as data to the server. then the size of "Soongsil University"
 is 19 bytes long, so 19 is an odd number; therefore, it received a reply from the server: "Error 403 Forbidden."
"""
import argparse, random, socket

MAX_BYTES = 65535


def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((interface, port))
    print('Listening at', sock.getsockname())
    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        if random.random() < 0.5:
            print('Pretending to drop packet from {}'.format(address))
            continue
        text = data.decode('ascii')
        print('The client at {} says {!r}'.format(address, text))
        if len(data) % 2 == 1:  # odd number
            message = 'Error 403 Forbidden.'.format(len(data))
        else:  # even number
            message = 'Your data was {} bytes long'.format(len(data))
        sock.sendto(message.encode('ascii'), address)


def client(hostname, port, text):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((hostname, port))
    print('Client socket name is {}'.format(sock.getsockname()))

    delay = 0.1  # seconds
    data = text.encode('ascii')
    while True:
        sock.send(data)
        print('Waiting up to {} seconds for a reply'.format(delay))
        sock.settimeout(delay)
        try:
            data = sock.recv(MAX_BYTES)
        except socket.timeout as exc:
            delay *= 2  # wait even longer for the next request
            if delay > 2.0:
                raise RuntimeError('I think the server is down') from exc
        else:
            break  # we are done, and can stop looping

    print('{}'.format(data.decode('ascii')))


if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive UDP,'
                                                 ' pretending packets are often dropped')
    parser.add_argument('role', choices=choices, help='which role to take')
    parser.add_argument('host', help='interface the server listens at;'
                                     ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='UDP port (default 1060)')
    parser.add_argument('-t', metavar='TEXT', type=str, default='',
                        help='format: \'TEXT\' text(data) that client sends to server\n ')
    args = parser.parse_args()
    function = choices[args.role]
    if function is client:
        function(args.host, args.p, args.t)
    else:
        function(args.host, args.p)
