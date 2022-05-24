import random
import time
import zmq

# publisher
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind(f'tcp://*:5555')

while True:
    topic_list = ['sports', 'technology', 'science']
    news_list = {"sports": ["soccer", "basketball", "baseball"],
                 "technology": ["network", "machine learning", "IoT"],
                 "science": ["physics", "biology"]}
    # randomly publish a news
    topic = random.choice(topic_list)
    news = random.choice(news_list.get(topic))

    # publish {topic}:{news} in message queue
    print(topic + ":" + news)
    socket.send((topic + ":" + news).encode('ascii'))
    time.sleep(0.5)
