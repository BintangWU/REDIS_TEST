import asyncio
import async_timeout
import json
import logging
import redis.asyncio as redis

CHANNEL_NAME = "ok"

logging.basicConfig(level=logging.DEBUG)


async def send_message(user_id: int, message: str):
    # write real code here
    logging.debug(f"Sending message to user {user_id}: {message}")
    await asyncio.sleep(0.2)


async def handle_notification(CH):
    r = redis.Redis(password= 'admin')
    pubsub = r.pubsub()
    await pubsub.subscribe(CH)
    while True:
        try:
            async with async_timeout.timeout(1):
                message = await pubsub.get_message()
                if message and message["type"] == "message":
                    payload = json.loads(message["data"])
                    # TODO: do validation on payload
                    await send_message(payload["user_id"], payload["message"])
        except (asyncio.TimeoutError, json.decoder.JSONDecodeError) as e:
            logging.error(e)


if __name__ == "__main__":
    asyncio.run(handle_notification(CHANNEL_NAME))