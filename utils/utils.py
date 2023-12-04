import os
import random
import time

import yaml


def load_config(config, config_file='config.yml'):
    for var in config:
        # 从环境变量加载配置
        config[var] = os.getenv(var)

        # 如果环境变量不存在，尝试从 YAML 文件加载配置
        if config[var] is None:
            try:
                with open(config_file, 'r') as file:
                    yaml_config = yaml.safe_load(file)
                    config[var] = yaml_config.get(var, '')
            except FileNotFoundError:
                print(f"{config_file} not found")
    print('配置文件:' + str(config))
    return config


def random_sleep_int(rs):
    rr = [0, 3600]
    ri = 0
    if rs is not None and rs != '':
        rr = str(rs).split('-')
    try:
        ri = random.randint(int(rr[0]), int(rr[1]))
    except Exception as e:
        print('随机延迟配置错误,请用0-3600的格式:' + str(e))
    return ri


def get_china_time(time_str):
    time_str = time_str[0:str(time_str).index('.')].replace('T', ' ')
    r_time = time.mktime(time.strptime(time_str, "%Y-%m-%d %H:%M:%S"))
    re = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(r_time + 28800))
    return re


def notify(ttui, title, content):
    if os.path.exists('notify.py'):
        import notify
        if ttui is not None and ttui != '':
            notify.push_config['TG_USER_ID'] = ttui
        notify.send(title, content)
    else:
        print(content)
