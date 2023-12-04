# -- coding:UTF-8 --
"""
cron: 0 0 * * *
new Env('哔哩哔哩 福利社抢会员兑换');
"""

import requests

from utils.utils import load_config, notify

TASK_NAME = '哔哩哔哩 福利社抢会员兑换'

config = {
    'Ray_BiliBiliCookies__0': '',
    'Ray_Security__UserAgent': '',
    'csrf': '',
    'TASKS_TG_USER_ID': ''
}

load_config(config)

headers = {
    'Host': 'app.bilibili.com',
    'Connection': 'keep-alive',
    'User-Agent': config.get('Ray_Security__UserAgent'),
    'Accept': '*/*',
    'Origin': 'https://www.bilibili.com',
    'X-Requested-With': 'tv.danmaku.bili',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.bilibili.com/blackboard/activity-new-freedata.html?share_source=COPY&share_plat=android&share_tag=s_i&url_from_h5=1%2C1&plat_id=124&share_from=h5&share_medium=android&unique_k=CNuA4FT&timestamp=1674795097&native.theme=1',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cookie': config.get('Ray_BiliBiliCookies__0'),
}

data = {
    'cross_domain': 'true',
    'id': '3',
    'csrf': config.get('csrf'),
}

response = requests.post('https://app.bilibili.com/x/wall/unicom/order/pack/receive', headers=headers, data=data)
notify(config.get('TASKS_TG_USER_ID'), TASK_NAME, str(response.json()))
