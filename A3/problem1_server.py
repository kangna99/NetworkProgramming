import asyncio, argparse, random

MAX_ATTEMPT = 5


@asyncio.coroutine
def server(reader, writer):
    address = writer.get_extra_info('peername')
    print('Accepted connection from {}'.format(address))

    # ans: a random number which will be initialized when the game is started
    # attempt: a number of chance to guess (should be under MAX_ATTEMPT)
    ans = 0
    attempt = 0

    while True:
        message = yield from reader.read(4096)
        message = str(message).split('\'')[1]

        # if client sends "start" or "end", the game begins
        if message == "start":
            print('game started')
            attempt = 0
            ans = random.randint(1, 10)
            print('The answer is {}'.format(ans))

        elif message == "end":
            print('game finished')
            continue

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

            writer.write(reply.encode('ascii'))

        elif message == "close":
            print('Client {} closed socket normally'.format(address))
            return

        # every other inputs except "start" or "end" or "close" or guess(int) makes an error message
        else:
            print('{}'.format(message))
            print('user input error')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='[server] "Guess the number" game over TCP')
    parser.add_argument('host', help='IP or hostname')
    parser.add_argument('-p', metavar='port', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    address = (args.host, args.p)
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(server, *address)
    server = loop.run_until_complete(coro)
    print('Listening at {}'.format(address))
    try:
        loop.run_forever()
    finally:
        server.close()
        loop.close()
