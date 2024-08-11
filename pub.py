import redis
import time

def publish_msg(channel, msgs):
    r = redis.Redis(host= 'localhost', password= 'admin', port= 6379)
    r.publish(channel= channel, message= msgs)
    print(f'Publish message {msgs} to channel {channel}')
    
if __name__ == '__main__':
    channel = 'myCh'
    
    while True:
        msgs = input('Enter msgs: ')
        if msgs.lower == 'exit':
            break
        publish_msg(channel, msgs)
        time.sleep(1)