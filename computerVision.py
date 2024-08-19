import cv2 as cv, numpy as np
from myredis import MyRedis

import asyncio
import requests


class ComputerVision():
    def __init__(self, img_source, username: str, password: str) -> None:
        self._source = img_source
        self._auth = (username, password)
    
    
    def crop_img(self, region: list, img):
        return img[region[1]:region[4], region[0]:region[2]]
    
    
    async def publish_image(selft, redis: MyRedis, topic: str, img):
        try:
            stat, bts = cv.imencode('.png', img)
            redis.publish(f'{topic}', bts.tobytes())
        except Exception as err:
            print(f'Error: \n{err}')


async def main(redis: MyRedis):
    pubsub = redis.pubsub()
    webCam = cv.VideoCapture(0)
    vis = ComputerVision(webCam, "admin", "admin")
    await asyncio.sleep(2)
    
    while(True):
        pubsub.get_message()
        respose = requests.get("https://wallpapers.com/images/featured/nature-2ygv7ssy2k0lxlzu.jpg", stream= tuple).raw
        img_raw = np.asarray(bytearray(respose.read()), dtype= 'uint8')
        img = cv.imdecode(img_raw, cv.IMREAD_COLOR)
        img_resize = cv.resize(img, (480,270), interpolation= cv.INTER_AREA)
        
        asyncio.create_task(vis.publish_image(redis, "cam1", img_resize))
        print("Running")
        
        await asyncio.sleep(0)


if __name__ == '__main__':
    db = MyRedis(password='admin')
    asyncio.run(main(db))



