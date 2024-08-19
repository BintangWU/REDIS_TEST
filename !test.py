# Subscriber (Viewer) Side
import cv2
import numpy as np
import redis

# Create Redis connection
redis_connection = redis.StrictRedis(host='localhost', port=6379, password= 'admin',db=0)

# Subscribe to a specific channel
def subscribe_to_camera(id):
    pubsub = redis_connection.pubsub()
    pubsub.subscribe(f'cam{id}:img')

    for message in pubsub.listen():
        if message['type'] == 'message':
            # Convert the byte stream back into a numpy array
            image_bytes = message['data']
            np_arr = np.frombuffer(image_bytes, np.uint8)

            # Decode the image
            image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            
            if image is not None:
                # Display the image or process it
                cv2.imshow(f'Camera {id} Stream', image)
                cv2.waitKey(1)
            else:
                print("Failed to decode image")

if __name__ == '__main__':
    subscribe_to_camera(1)
# subscribe_to_camera(1)
