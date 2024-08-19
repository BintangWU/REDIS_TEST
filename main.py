import os, sys, argparse
import asyncio


def redisCon_parse(input: str):
    _input = input.split(':')
    _host = _input[0]
    _port = _input[1]
    return _host, _port


if __name__ == '__main__':
    parse = argparse.ArgumentParser(description= 'Stream IP camera HIK Vision -> Redis')
    parse.add_argument('--redis', type= str, default= '127.0.0.1:6379', help= 'Redis IP:PORT <127.0.0.1:6379>')
    parse.add_argument('--source', type= str, default= '0', help= 'RTSP source')
    parse.add_argument('--camera-num', type= int, default= 0, help= 'Number of camera, which one do you want to use the camera..')
    opt = parse.parse_args()
    
    camera_number = f'cam{opt.camera_num}'
    camera_source = opt.source
    redis_host, redis_port = redisCon_parse(opt.redis)
    
    # print(camera_number, camera_source, redis_host, redis_port)