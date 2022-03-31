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
import argparse, socket

MAX_BYTES = 65535


def server(interface, port):
    # create socket as Address Family = IPv4 , Socket Type = UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # bind socket
    sock.bind((interface, port))
    print('Listening at', sock.getsockname())
    while True:
        # recvfrom() returns (bytes, address) in tuple
        data, address = sock.recvfrom(MAX_BYTES)
        # data should be decoded
        text = data.decode('ascii')
        print('The client at {} says {!r}'.format(address, text))
        # reply message to client depends on the text length
        if len(text) % 2 == 1:  # odd number
            message = 'Error 403 Forbidden.'.format(len(text))
        else:  # even number
            message = 'Your data was {} bytes long'.format(len(text))

        # socket sends response after encoding
        sock.sendto(message.encode('ascii'), address)


def client(hostname, port):
    # create socket as Address Family = IPv4 , Socket Type = UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # connect socket
    sock.connect((hostname, port))
    print('Client socket name is {}\n'.format(sock.getsockname()))
    # client inputs data and encode it in 'ascii'
    text = input('input data>> ')
    data = text.encode('ascii')
    # send data to the server
    sock.send(data)
    # socket receives response from the server
    data = sock.recv(MAX_BYTES)
    print('{}'.format(data.decode('ascii')))


if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive UDP')
    parser.add_argument('role', choices=choices, help='which role to take')
    parser.add_argument('host', help='interface the server listens at;'
                                     ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='UDP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)
