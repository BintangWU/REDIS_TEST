import redis, logging, time, os
from redis.commands.json.path import Path
from typing import Optional, Union, Any


class MyRedis(redis.Redis):
    def __init__(self, host: str = 'localhost', port: int = 6379, user: Optional[str] = None, pwd: Optional[str] = None, debug: bool = False) -> None:
        super().__init__(host= host, port= port, username= user, password= pwd, decode_responses= True)
        self._pubsub = self.pubsub()
        
        self._time = time.strftime("%Y%m%d_%I%p")
        self._log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs/redis_con')
        self._log_name = f"REDIS-CON_{self._time}.log"
        
        if not os.path.exists(self._log_dir):
            os.mkdir(self._log_dir)
        
        logging.basicConfig(
            level= logging.INFO,
            filename= os.path.join(self._log_dir, self._log_name),
            format= "[%(asctime)s] %(levelname)s: %(message)s"
        )
        
        self._console = logging.StreamHandler()
        self._console.setLevel(logging.DEBUG)
        self._console.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s"))
        
        self._logger = logging.getLogger("REDIS-CON")
        self._logger.addHandler(self._console)
        self._logger.info("Begin connection!!!")
        
        self._debug = debug
        
        
    # Test connection to Redis
    def test_connection(self) -> bool:
        return self.ping()
    
    
    # Write string data to Redis (write adn update)
    # print(myRedis.set_string("HELO", "WORLD"))
    def set_value(self, *args) -> bool:
        try: 
            if len(args) == 1 and isinstance(args[0], dict):
                return self.mset(args[0])
            elif len(args) == 2:
                if not isinstance(args[0], dict):
                    return self.set(args[0], args[1])
                else:
                    raise Exception(f"Sorry, the value of args[0]) is {type(args[0])}")
            else:
                raise Exception("Sorry, set_value(*args) out of range!")

        except Exception as err:
            self._logger.error(err)
            return None
    

    # Write json data to Redis
    # myRedis.set_json("test", value= data)
    def set_json(self, key: str, **kwargs) -> bool:
        if 'path' in kwargs:
            return self.json().set(key, Path(kwargs['path']), kwargs['value'])
        else:
            return self.json().set(key, '$', kwargs['value'])


    # Read string data from Redis
    def get_value(self, *args) -> Any:
        data = None
        try: 
            if len(args) == 1:
                data = self.get(args[0])
            else:
                data = self.mget(*args)
            return data
        
        except Exception as err:
            self._logger.error(err)
            return None

    
    # Read JSON data from Redis
    # print(myRedis.get_json("cam2:region", '[0]["region"]'))
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
            self._logger.error(err)
            return None
    
    
    def pub(self, ch: Union[bytes, str, memoryview], msg: Union[str, int, float, bytes]) -> None:
        self.publish(channel= ch, message= msg)
        
        
    # def sub(self, ch):
    #     self._pubsub.subscribe(ch)
    #     return self._pubsub.listen()['data']
    
class Async_MyRedis(redis.asyncio.Redis):
    def __init__(self, host: str = 'localhost', port: int = 6379, user: Optional[str] = None, pwd: Optional[str] = None, debug: bool = False) -> None:
        super().__init__(host= host, port= port, username= user, password= pwd, decode_responses= True)    
        

if __name__ == "__main__":
    myRedis = MyRedis(pwd= "admin")
    
    dict_data = {
        "employee_name": "Adam Adams",
        "employee_age": 30,
        "position": "Software Engineer",
    }
    # myRedis.set_value("aloha", dict_data)



    
    
    
    