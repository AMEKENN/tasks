# -- coding:UTF-8 --
"""
cron: 0 12 * * *
new Env('Emby保持活动');
"""
import asyncio

import requests

from utils.utils import load_config, random_sleep_int, get_china_time, notify

TASK_NAME = 'Emby保持活动'

config = {
    'EMBY_DEFAULT_USERNAME': '',
    'EMBY_DEFAULT_PASSWORD': '',
    'EMBY_DEFAULT_DEVICE_ID': '',
    'EMBY_DEFAULT_USER_AGENT': '',
    'EMBY_DEFAULT_INFO': '',
    "EMBY": '',
    'TASKS_TG_USER_ID': '',
    'RANDOM_SLEEP': ''
}
load_config(config)


class Emby:

    def __init__(self, url, username, password, device_id, user_agent, info):
        self.url = url
        self.username = username
        self.password = password
        self.device_id = device_id
        self.user_agent = user_agent
        self.info = info

    def __repr__(self):
        return 'Emby(%s, %s,%s,%s, %s,%s)' % (
            self.url, self.username, self.password,
            self.device_id, self.user_agent, self.info)

    # 登录
    def auth(self):
        headers = {
            "Connection": "keep-alive",
            "Content-Length": "28",
            "accept": "application/json",
            "User-Agent": str(self.user_agent),
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "com.mb.android.tg",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        params = {
            "X-Emby-Client": "Emby for Android",
            "X-Emby-Device-Name": "Android",
            "X-Emby-Device-Id": str(self.device_id),
            "X-Emby-Client-Version": "3.2.32-17.15"
        }
        data = {
            'Username': str(self.username),
            'Pw': str(self.password)
        }
        response = requests.post(str(self.url) + '/emby/Users/authenticatebyname',
                                 headers=headers, params=params, data=data)
        if response.status_code != 200:
            raise Exception('登陆出错' + str(response))
        return response

    def full(self, token):
        headers = {
            "Connection": "keep-alive",
            # "Content-Length": "3145",
            "User-Agent": str(self.user_agent),
            "Content-Type": "text/plain",
            "Accept": "*/*",
            "X-Requested-With": "com.mb.android.tg",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        params = {
            "X-Emby-Client": "Emby for Android",
            "X-Emby-Device-Name": "Android",
            "X-Emby-Device-Id": str(self.device_id),
            "X-Emby-Client-Version": "3.2.32-17.15",
            "X-Emby-Token": token,
            "reqformat": "json"
        }
        data = '{"PlayableMediaTypes":["Audio","Video"],"SupportedCommands":["MoveUp","MoveDown","MoveLeft",' \
               '"MoveRight","PageUp","PageDown","PreviousLetter","NextLetter","ToggleOsd","ToggleContextMenu",' \
               '"Select","Back","SendKey","SendString","GoHome","GoToSettings","VolumeUp","VolumeDown","Mute",' \
               '"Unmute","ToggleMute","SetVolume","SetAudioStreamIndex","SetSubtitleStreamIndex",' \
               '"RefreshMediaSource","DisplayContent","GoToSearch","DisplayMessage","SetRepeatMode",' \
               '"SetSubtitleOffset","SetPlaybackRate","ChannelUp","ChannelDown","PlayMediaSource","PlayTrailers"],' \
               '"SupportsMediaControl":true,"DeviceProfile":{"MaxStaticBitrate":200000000,' \
               '"MaxStreamingBitrate":200000000,"MusicStreamingTranscodingBitrate":192000,' \
               '"MaxStaticMusicBitrate":10000000,"DirectPlayProfiles":[{"Type":"Video","VideoCodec":null},' \
               '{"Type":"Audio","Container":"mp4,m4a,aac,ac3"},{"Type":"Audio","Container":"webm"},{"Type":"Audio",' \
               '"Container":"mka,mkv"},{"Type":"Audio","Container":"mp3"},{"Type":"Audio","Container":"opus,ogg,' \
               'oga"},{"Type":"Audio","Container":"wav,wave"},{"Type":"Audio","Container":"mpg,mpeg,ps,m2p"},' \
               '{"Type":"Audio","Container":"ts,tsa"},{"Type":"Audio","Container":"flac"},{"Type":"Audio",' \
               '"Container":"amr,3ga"}],"TranscodingProfiles":[{"Container":"ts","Type":"Video","AudioCodec":"ac3,' \
               'aac,mp3","VideoCodec":"h264,mpeg2video,hevc","Context":"Streaming","Protocol":"hls",' \
               '"MaxAudioChannels":"6","MinSegments":"1","BreakOnNonKeyFrames":true,"SegmentLength":"3",' \
               '"ManifestSubtitles":"vtt"},{"Container":"ts","Type":"Audio","AudioCodec":"aac","Context":"Streaming",' \
               '"Protocol":"hls","MinSegments":"1","SegmentLength":"3","BreakOnNonKeyFrames":true},' \
               '{"Container":"mp3","Type":"Audio","AudioCodec":"mp3","Context":"Streaming","Protocol":"http"},' \
               '{"Container":"mkv","Type":"Video","AudioCodec":"aac,mp3,ac3","VideoCodec":"h264","Context":"Static",' \
               '"MaxAudioChannels":"2"},{"Container":"mp3","Type":"Audio","AudioCodec":"mp3","Context":"Static",' \
               '"Protocol":"http","MaxAudioChannels":"2"}],"ContainerProfiles":[],"CodecProfiles":[{"Type":"Video",' \
               '"Codec":"hevc","Conditions":[{"Condition":"EqualsAny","Property":"VideoProfile","Value":"Main|Main ' \
               '10|Rext","IsRequired":false}]},{"Type":"Video","Codec":"h264","Conditions":[{' \
               '"Condition":"LessThanEqual","Property":"VideoLevel","Value":"51","IsRequired":false}]}],' \
               '"SubtitleProfiles":[{"Format":"vtt","Method":"Hls"},{"Format":"srt","Method":"External"},' \
               '{"Format":"ssa","Method":"External"},{"Format":"ass","Method":"External"},{"Format":"smi",' \
               '"Method":"External"},{"Format":"srt","Method":"Embed"},{"Format":"subrip","Method":"Embed"},' \
               '{"Format":"ass","Method":"Embed"},{"Format":"ssa","Method":"Embed"},{"Format":"dvb_teletext",' \
               '"Method":"Embed"},{"Format":"dvb_subtitle","Method":"Embed"},{"Format":"dvbsub","Method":"Embed"},' \
               '{"Format":"pgs","Method":"Embed"},{"Format":"pgssub","Method":"Embed"},{"Format":"dvdsub",' \
               '"Method":"Embed"},{"Format":"vtt","Method":"Embed"},{"Format":"sub","Method":"Embed"},' \
               '{"Format":"idx","Method":"Embed"},{"Format":"smi","Method":"Embed"}],"ResponseProfiles":[]},' \
               '"IconUrl":"https://github.com/MediaBrowser/Emby.Resources/raw/master/images/devices/android.png",' \
               '"SupportsSync":true,"SupportsContentUploading":true}'
        response = requests.post(str(self.url) + '/emby/Sessions/Capabilities/Full',
                                 headers=headers, params=params, data=data)
        if response.status_code != 204:
            raise Exception('更新信息出错' + str(response))
        return response

    def user(self, token, userid):
        headers = {
            "Connection": "keep-alive",
            "User-Agent": str(self.user_agent),
            "X-Requested-With": "com.mb.android.tg",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        params = {
            "X-Emby-Client": "Emby for Android",
            "X-Emby-Device-Name": "Android",
            "X-Emby-Device-Id": str(self.device_id),
            "X-Emby-Client-Version": "3.2.32-17.15",
            "X-Emby-Token": token,
        }
        response = requests.get(str(self.url) + '/emby/Users/' + userid,
                                headers=headers, params=params)
        if response.status_code != 200:
            raise Exception('获取用户信息出错' + str(response))
        return response

    def logout(self, token):
        headers = {
            "Connection": "keep-alive",
            # "Content-Length": "0",
            "User-Agent": str(self.user_agent),
            "Accept": "*/*",
            "X-Requested-With": "com.mb.android.tg",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        params = {
            "X-Emby-Client": "Emby for Android",
            "X-Emby-Device-Name": "Android",
            "X-Emby-Device-Id": str(self.device_id),
            "X-Emby-Client-Version": "3.2.32-17.15",
            "X-Emby-Token": token
        }
        response = requests.post(str(self.url) + '/emby/Sessions/Logout',
                                 headers=headers, params=params)
        if response.status_code != 204:
            raise Exception('登出出错' + str(response))
        return response


async def active(emby: Emby):
    rs = random_sleep_int(config.get('RANDOM_SLEEP'))
    await asyncio.sleep(rs)
    token = None
    msg = '延迟执行:' + str(rs) + 's' + \
          '\n服务器:' + emby.url
    try:
        # 登陆
        auth = emby.auth()
        auth_json = auth.json()
        token = auth_json['AccessToken']
        userid = auth_json['User']['Id']
        last_login_date = auth_json['User']['LastLoginDate']
        last_activity_date = auth_json['User']['LastActivityDate']
        # 更新信息
        emby.full(token)
        msg = msg + \
              '\n最后登录时间:' + get_china_time(last_login_date) + \
              '\n最后活动时间:' + get_china_time(last_activity_date) + \
              '\n' + str(emby.info)
    # 异常处理
    except Exception as e:
        msg = msg + "活跃失败:" + str(e)

    if token is not None:
        try:
            emby.logout(token)
        except Exception as e:
            msg = msg + '\n' + str(e)

    notify(config.get('TASKS_TG_USER_ID'), TASK_NAME, msg)


def get_embys():
    emby_str = config.get('EMBY').split('&')
    embys = []
    for i in emby_str:
        try:
            # 解析emby属性
            emby_dic = {}
            for j in i.split(";"):
                s = j.split("=")
                emby_dic[s[0]] = s[1]
            # 赋值属性
            url = emby_dic['url']
            username = config.get('EMBY_DEFAULT_USERNAME')
            password = config.get('EMBY_DEFAULT_PASSWORD')
            device_id = config.get('EMBY_DEFAULT_DEVICE_ID')
            user_agent = config.get('EMBY_DEFAULT_USER_AGENT')
            info = config.get('EMBY_DEFAULT_INFO')

            if 'username' in emby_dic and emby_dic['username']:
                username = emby_dic['username']
            if 'password' in emby_dic and emby_dic['password']:
                password = emby_dic['password']
            if 'device_id' in emby_dic and emby_dic['device_id']:
                device_id = emby_dic['device_id']
            if 'user_agent' in emby_dic and emby_dic['user_agent']:
                user_agent = emby_dic['user_agent']
            if 'info' in emby_dic and emby_dic['info']:
                info = emby_dic['info']

            emby = Emby(url, username, password, device_id, user_agent, info)
            embys.append(emby)
        except Exception as e:
            print('配置文件可能有误\n请检查:' + str(i) + ' ' + str(e))
    return embys


def main():
    embys = get_embys()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = []
    for i in embys:
        tasks.append(asyncio.ensure_future(active(i)))
    loop.run_until_complete(asyncio.wait(tasks))


if __name__ == "__main__":
    main()
