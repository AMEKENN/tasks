import os
import random
import time

import yaml

config = {
    'TASKS_TG_USER_ID': '',
    'RANDOM_SLEEP': '',
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


def random_sleep_int():
    rs = config.get('RANDOM_SLEEP')
    rr = [0, 3600]
    if rs is not None and rs != '':
        rr = str(rs).split('-')
    try:
        ri = random.randint(int(rr[0]), int(rr[1]))
        return ri
    except Exception as e:
        print('随机延迟配置错误,请用0-3600的格式:' + str(e))


def get_china_time(time_str):
    time_str = time_str[0:str(time_str).index('.')].replace('T', ' ')
    r_time = time.mktime(time.strptime(time_str, "%Y-%m-%d %H:%M:%S"))
    re = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(r_time + 28800))
    return re


def notify(title, content):
    if os.path.exists('notify.py'):
        import notify
        ttui = config.get('TASKS_TG_USER_ID')
        if ttui is not None and ttui != '':
            notify.push_config['TG_USER_ID'] = ttui
        notify.send(title, content)
    else:
        print(content)


def get_config():
    return config
