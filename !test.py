import redis

r = redis.Redis(password= 'admin', decode_responses= True)

def redis_set(*args):
    if len(args) == 1 and isinstance(args[0], dict):
        # print(args[0])
        r.mset(args[0])
    elif len(args) == 2:
        if not isinstance(args[0], dict):
            # print(args[0], args[1])
            r.set(args[0], args[1])
        else:
            raise Exception(f"Sorry, the value of args[0]) is {type(args[0])}")
    else:
        raise Exception("Sorry, redis_set(*args) out of range ")

def redis_get(*args):
    print(r.mget(*args))

dict_data = {
        "employee_name": "Adam ams",
        "employee_age": 30,
        "position": "Software Engineer",
    }

if __name__ == '__main__':
    redis_get("employee_name", "employee_age", "position", "non_existing")