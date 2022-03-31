"""
3. [4 points] Write a Python script to create a TCP Server and Client using python socket standard library to develop a game "Guess the number."

The game will follow as :
1) The server will choose a random number between 1 to 10.
2) Inform the client and ask to guess a number between 1 to 10.
3) Client will send a guessed number as a request to the server.

Conditions:
1) Client will request to start the game by sending the first request as "start."
2) Client will have only 5 attempts to guess the correct number
3) The client will only win if he guesses the correct number within 5 attempts and loses the game.

The exchange of messages between server and client during the game will follow the following conditions and message text based on the difference of actual number with server and guessed number by client:

x = random chosen number by server
guess = number guessed by a client

conditions and messages:
(x = guess) -> "Congratulations you did it."
(x > guess) -> "You guessed too small!"
(x < guess) -> "You Guessed too high!"
"""

import argparse, random, socket
import os


def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Address Family = IPv4 , Socket Type = TCP connection
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # to resolve problem when port is used
    sock.bind((interface, port))
    sock.listen(1)
    print('Listening at', sock.getsockname())
    ans = random.randint(1, 10)
    print('ans: {}'.format(ans))
    attempt_cnt = 0
    print('Waiting to accept a new connection')
    sc, sockname = sock.accept()  # accept returns (socket, addr) tuple
    print('We have accepted a connection from', sockname)
    print('  Socket name:', sc.getsockname())
    print('  Socket peer:', sc.getpeername())
    while True:
        message = sc.recv(1024).decode('ascii')
        print(message)
        if message == "start":
            print('game started')

        elif message.isdigit():
            guess = int(message)
            print('client guess: {}'.format(guess))

            if guess == ans:
                reply = "Congratulations you did it."
            elif guess > ans:
                reply = "You Guessed too high!"
            else:
                reply = "You guessed too small!"

            sc.sendall(reply.encode('ascii'))
            # if reply == "Congratulations you did it.":
            #     sc.close()
            #     sock.close()
            # else:
            #     attempt_cnt += 1

        elif message == "close":
            sc.close()
            sock.close()
            break

        else:
            print('user input error')
            sc.close()

        # if attempt_cnt == 5:
        #     sc.sendall(b'Farewell, client')
        #     sc.close()
        #     print('  Reply sent, socket closed')


def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create socket
    sock.connect((host, port))  # connect socket
    while True:
        user_input = input("Type \"start\" to begin the game!\n>> ")
        if user_input == "start":
            sock.sendall(user_input.encode('ascii'))
            os.system('cls')
            break
        else:
            print("check your input (type \"start\")")
            continue
    guess_cnt = 1
    print('you have only 5 chances to guess the number! (1~10)')

    while True:
        user_input = input("guess the number>> ")
        if user_input.isdigit():  # if the input is digit follow below
            if 1 <= int(user_input) <= 10:
                sock.sendall(str(user_input).encode('ascii'))
                reply = sock.recv(1024).decode('ascii')
                print(repr(reply))
                if reply == "Congratulations you did it.":
                    print("\nYou made it in {} try!!".format(guess_cnt))
                    break

                guess_cnt += 1
            else:
                print('check the number range (1~10)')
                continue

            if guess_cnt > 5:
                break
        else:  # else if the input is not digit continue and ask client to 'guess the number' again
            continue
    sock.sendall(b'close')
    sock.close()


if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='"Guess the number" game over TCP')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;'
                                     ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)
