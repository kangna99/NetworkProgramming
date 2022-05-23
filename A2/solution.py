import json
import zlib
import socket
import ssl


class Solution():

    def special_bits(self, L=1, R=2, k=1):
        num = -2
        # Write your code between start and end for solution of problem 1
        # Start
        for i in range(L, R + 1):
            if k == bin(i).count('1'):  # if '1' count in binary matches, break the loop
                num = i
                break
            else:  # else return value should be '-1'
                num = -1
        # End
        return num

    def toggle_string(self, S):
        s = ""
        # Write your code between start and end for solution of problem 2
        # Start
        # dictionary to match lowercase to uppercase
        lower2Upper = {"a": "A", "b": "B", "c": "C", "d": "D", "e": "E", "f": "F", "g": "G",
                       "h": "H", "i": "I", "j": "J", "k": "K", "l": "L", "m": "M", "n": "N",
                       "o": "O", "p": "P", "q": "Q", "r": "R", "s": "S", "t": "T", "u": "U",
                       "v": "V", "w": "W", "x": "X", "y": "Y", "z": "Z"}
        # dictionary to match uppercase to lowercase
        upper2Lower = {"A": "a", "B": "b", "C": "c", "D": "d", "E": "e", "F": "f", "G": "g",
                       "H": "h", "I": "i", "J": "j", "K": "k", "L": "l", "M": "m", "N": "n",
                       "O": "o", "P": "p", "Q": "q", "R": "r", "S": "s", "T": "t", "U": "u",
                       "V": "v", "W": "w", "X": "x", "Y": "y", "Z": "z"}
        for c in S:
            if 'a' <= c <= 'z':  # lower case -> upper case
                s += lower2Upper[c]
            elif 'A' <= c <= 'Z':  # upper case -> lower case
                s += upper2Lower[c]
            else:
                s += c

        ## not allowed because of predefined functions e.g. ord(), chr() ##
        # for c in S:
        #     if 'a' <= c <= 'z':  # lower case -> upper case
        #         s += chr(ord(c) - 32)
        #     elif 'A' <= c <= 'Z':  # upper case -> lower case
        #         s += chr(ord(c) + 32)
        #     else:
        #         s += c
        # End
        return s

    def send_message(self, message):
        message = self.to_json(message)
        message = self.encode(message)
        message = self.compress(message)
        return message

    def recv_message(self, message):
        message = self.decompress(message)
        message = self.decode(message)
        message = self.to_python_object(message)
        return message

    # String to byte
    def encode(self, message):
        # Write your code between start and end for solution of problem 3
        # Start
        return message.encode("utf-8")
        # End

    # Byte to string
    def decode(self, message):
        # Write your code between start and end for solution of problem 3
        # Start
        return message.decode("utf-8")
        # End 

    # Convert from python object to json string
    def to_json(self, message):
        # Write your code between start and end for solution of problem 3
        # Start
        return json.dumps(message)
        # End 

    # Convert from json string to python object
    def to_python_object(self, message):
        # Write your code between start and end for solution of problem 3
        # Start
        return json.loads(message)
        # End 

    # Returns compressed message 
    def compress(self, message):
        # Write your code between start and end for solution of problem 3
        # Start
        return zlib.compress(message)
        # End 

    # Returns decompressed message
    def decompress(self, compressed_message):
        # Write your code between start and end for solution of problem 3
        # Start
        return zlib.decompress(compressed_message)
        # End 

    def client(self, host, port, cafile=None):
        # Write your code between start and end for solution of problem 4
        # Start
        cert = ""  # Variable to store the certificate received from server
        cipher = ""  # Variable to store cipher used for connection
        msg = ""  # Variable to store message received from server

        # client to authenticate server with crt file
        purpose = ssl.Purpose.SERVER_AUTH
        context = ssl.create_default_context(purpose, cafile=cafile)
        context.check_hostname = False

        # TCP connection
        raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        raw_sock.connect((host, port))
        # Wrap a raw socket using ssl
        ssl_sock = context.wrap_socket(raw_sock, server_hostname=host)

        # read certificate
        cert = ssl_sock.getpeercert()
        # read cipher
        cipher = ssl_sock.cipher()
        # read the data received from the server
        while True:
            data = ssl_sock.recv(1024)
            if not data:
                break
            msg += data.decode("utf-8")  # decode byte to string
        # End
        return cert, cipher, msg
