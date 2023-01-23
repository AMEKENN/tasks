import os
import random
import time

import yaml

config = {
    'SLEEP_RANGE': '',
    'EMBY_DEFAULT_USERNAME': '',
    'EMBY_DEFAULT_PASSWORD': '',
    'EMBY_DEFAULT_DEVICE_ID': '',
    'EMBY_DEFAULT_USER_AGENT': '',
    'EMBY_DEFAULT_INFO': '',
    "EMBY": ''
}
if os.path.exists('config.yml'):
    with open('config.yml', 'r', encoding='utf-8') as f:
        s = f.read()
        j = yaml.load(s, Loader=yaml.SafeLoader)
        for k in config:
            if k in j and j[k]:
                v = j[k]
                config[k] = v

for k in config:
    if os.getenv(k):
        v = os.getenv(k)
        config[k] = v

print('配置文件:' + str(config))


def random_sleep(a, b):
    time.sleep(random.randint(a, b))


def get_china_time(time_str):
    time_str = time_str[0:str(time_str).index('.')].replace('T', ' ')
    r_time = time.mktime(time.strptime(time_str, "%Y-%m-%d %H:%M:%S"))
    re = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(r_time + 28800))
    return re


def notify(title, content):
    if os.path.exists('notify.py'):
        from notify import send
        send(title, content)
    else:
        print(content)


def get_config():
    return config
