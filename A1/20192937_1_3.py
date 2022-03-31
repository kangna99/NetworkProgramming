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

MAX_ATTEMPT = 5


def server(interface, port):
    # create socket as Address Family = IPv4 , Socket Type = TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # to resolve problem when port is used
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # bind socket
    sock.bind((interface, port))
    # listening socket is connected
    sock.listen(1)
    print('Listening at', sock.getsockname())
    print('Waiting to accept a new connection')
    # accept() returns (socket, address) in tuple
    sc, sockname = sock.accept()
    print('We have accepted a connection from', sockname)
    print('  Socket name:', sc.getsockname())
    print('  Socket peer:', sc.getpeername())

    # ans: a random number which will be initialized when the game is started
    # attempt: a number of chance to guess (should be under MAX_ATTEMPT)
    ans = 0
    attempt = 0

    while True:
        message = sc.recv(1024).decode('ascii')
        # if client sends "start", the game begins
        if message == "start":
            print('game started')
            attempt = 0
            ans = random.randint(1, 10)
            print('The answer is {}'.format(ans))

        # if client sends a number, reply message depends on the value
        elif message.isdigit():
            guess = int(message)
            attempt += 1
            print('{}try) {}'.format(attempt, guess))

            if guess == ans:
                reply = 'Congratulations you did it.'
                print('game over')
            elif attempt == MAX_ATTEMPT:
                print('game over')
                reply = "You lost the game!"
            elif guess > ans:
                reply = "You Guessed too high!"
            elif guess < ans:
                reply = "You guessed too small!"
            else:
                reply = "unknown condition"

            sc.sendall(reply.encode('ascii'))
        # every other inputs except "start" or guess(int) makes an error message
        else:
            print('user input error')


def client(host, port):
    # create socket as Address Family = IPv4 , Socket Type = TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect socket
    sock.connect((host, port))

    while True:
        user_input = input("Type \"start\" to begin the game!\n>> ")
        if user_input == "start":
            sock.sendall(user_input.encode('ascii'))
            os.system('cls')
            start = 1
            guess_cnt = 0
        else:
            print("check your input (type \"start\")")
            continue

        print('you have only 5 chances to guess the number! (1~10)')
        while start:
            user_input = input("guess the number>> ")
            # if the input is digit, follow below
            if user_input.isdigit():
                if 1 <= int(user_input) <= 10:
                    guess_cnt += 1
                    sock.sendall(str(user_input).encode('ascii'))
                    reply = sock.recv(1024).decode('ascii')
                    print(repr(reply))

                    # if client wins or loses the game, which means the game ended, break the loop
                    if reply == "Congratulations you did it.":
                        print("\nYou made it in {} try!!\n".format(guess_cnt))
                        break
                    if reply == "You lost the game!":
                        break

                # if the input is out of range 1~10
                else:
                    print('check the number range (1~10)')
                    continue

            # if the input is not digit, continue and ask client to 'guess the number' again
            else:
                continue


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
