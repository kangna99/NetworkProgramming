import argparse, socket, os

game = 0


def client(host, port):
    # create socket as Address Family = IPv4 , Socket Type = TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect socket
    sock.connect((host, port))

    while True:
        user_input = input("Type \"start\" to begin the game!\n(type \"close\" to exit)\n>> ")
        if user_input == "start":
            sock.sendall(user_input.encode('ascii'))
            os.system('cls')
            game = 1
            guess_cnt = 0
        elif user_input == "close":
            sock.sendall(user_input.encode('ascii'))
            sock.close()
            break
        else:
            print("check your input (type \"start\" or \"close\")")
            continue

        print('you have only 5 chances to guess the number! (1~10)\n(type \"end\" to finish the game)\n')
        while game:
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

            # if client wants to end the game and restart a new game
            elif user_input == "end":
                sock.sendall(user_input.encode('ascii'))
                break

            # if the input is not "end" or digit, continue and ask client to 'guess the number' again
            else:
                continue


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='[client] "Guess the number" game over TCP')
    parser.add_argument('host', help='IP or hostname')
    parser.add_argument('-p', metavar='port', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    client(args.host, args.p)
