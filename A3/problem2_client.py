import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5555")

# client chooses news topic
while True:
    user_input = input('topic: "sports", "technology", "science"\nselect topic >>')
    if user_input == "sports" or user_input == "technology" or user_input == "science":
        break
    else:
        continue

# subscribe news according to a chosen topic
if user_input == "sports":
    socket.setsockopt(zmq.SUBSCRIBE, b'sports')
elif user_input == "technology":
    socket.setsockopt(zmq.SUBSCRIBE, b'technology')
elif user_input == "science":
    socket.setsockopt(zmq.SUBSCRIBE, b'science')

# receive subscribe news
while True:
    message = socket.recv()
    print("%s" % message.decode('ascii').split(':')[1])
    time.sleep(1)
