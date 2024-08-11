import redis
from redis.commands.json.path import Path
from pydantic import BaseModel
from typing import Optional, Any


class MyRedis(redis.Redis):
    def __init__(self, host: str = 'localhost', port: int = 6379, user: Optional[str] = None, pwd: Optional[str] = None, debug: bool = False) -> None:
        super().__init__(host= host, port= port, username= user, password= pwd, decode_responses= True)
        
        # self.redis_con = redis.Redis(host= host, port= port, username= user, password= pwd, decode_responses= True)
        self._debug = debug
        
        
    # Test connection to Redis
    def test_connection(self) -> bool:
        return self.ping()
    
    
    # Write string data to Redis (write adn update)
    def set_string(self, key: str, value: str) -> bool:
        return self.set(key, value)
    

    # Write json data to Redis
    def set_json(self, key: str, **kwargs) -> bool:
        if 'path' in kwargs:
            return self.json().set(key, Path(kwargs['path']), kwargs['value'])
        else:
            return self.json().set(key, '$', kwargs['value'])


    # Read string data from Redis
    def get_string(self, key: str) -> str:
        try:
            data = self.get(key)
            if data is None:
                raise Exception(f"Value from \"{key}\" is None")
            else:
                return data
            
        except Exception as err:
            if self._debug:
                print(err)
            return None

    
    # Read JSON data from Redis
    def get_json(self, key: str, path: Optional[str] = None) -> Optional[Any]:
        try:             
            data = (self.json().get(key) if path == None else self.json().get(key, Path(path)))
            
            if data is None or data == []:
                raise Exception(f"Value from \"{key}\" is None")
            else:
                return data
            
        except Exception as err:
            if self._debug:
                print(err)
            return None
            

if __name__ == "__main__":
    myRedis = MyRedis(pwd= "admin")
    # print(myRedis.get_string("cam1:region"))
    # print(myRedis.get_json("cam2:region"))
    # print(myRedis.set_string("HELO", "WORLD"))
    myRedis.pubsub().subscribe()
    
    
    
    
    