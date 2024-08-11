from myredis import MyRedis
import time

def subscribe_msg(channel):
    r = redis.Redis(host= 'localhost', password= 'admin', port= 6379, decode_responses= True)
    pupsub = r.pubsub()
    pupsub.subscribe(channel)
    
    # print(pupsub.listen())
    for  message in pupsub.listen():
        print(f"Received message: { message}")
    
if __name__ == '__main__':
    channel = 'myCh'
    subscribe_msg(channel)
    
    