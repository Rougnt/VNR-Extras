# coding: utf8
# 5/19/2013 jichi
# fix 5/25/2019 owl
# Official: http://developer.baidu.com/wiki/index.php?title=帮助文档首页/百度翻译/翻译API
# Unofficial: https://gist.github.com/binux/1446348
#
# See: http://fanyi.baidu.com/static/i18n/zh/widget/translate/main/translateio/translateio.js
# See: http://fanyi.baidu.com/static/mobile/widget/translate-mobile/main/translateout/translateout.js
if __name__ == '__main__':
  import sys
  sys.path.append('..')

import json
import requests
import settings
import hashlib
import urllib
import ctypes
import math
import re
from numpy import *
from sakurakit.skdebug import dwarn, derror
import js2py
import os

path = os.path.dirname(__file__)
with open(path + '/sign.js') as fp:
    js = fp.read()
    context = js2py.EvalJs()
    context.execute(js)
    getToken = context.token

appid = settings.global_().getBaiduAppID()  # 你的appid
secretKey = settings.global_().getBaiduKey()  # 你的密钥


class Moemi:
    def __init__(self):
        self.sess = requests.Session()
        self.headers = {
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }
        self.token = None
        self.gtk = None
        
        self.loadMainPage()
        self.loadMainPage()
 
    def loadMainPage(self):
        """
            load main page : https://fanyi.baidu.com/
            and get token, gtk
        """
        url = 'https://fanyi.baidu.com'
 
        try:
            r = self.sess.get(url, headers=self.headers)
            self.token = re.findall(r"token: '(.*?)',", r.text)[0]
            self.gtk = re.findall(r"window.gtk = '(.*?)';", r.text)[0]
        except Exception, e:
            derror(e)

    def jp2zh(self, query):
        """
            max query count = 2
            get translate result from https://fanyi.baidu.com/v2transapi
        """
        url = 'https://fanyi.baidu.com/v2transapi'
 
        sign = getToken(query, self.gtk)
 
        data = {
            'from': 'jp',
            'to': 'zh',
            'query': query,
            'simple_means_flag': 3,
            'sign': sign,
            'token': self.token,
        }
        try:
            r = self.sess.post(url=url, data=data)
        except Exception, e:
            derror(e)
        
        if r.status_code == 200:
            json = r.json()
            if 'error' in json:
                raise Exception('baidu sdk error: {}'.format(json['error']))
            return json["trans_result"]["data"][0]['dst']
        return None
 
def translate(text, to='zhs', fr='ja'):
    if settings.global_().isBaiduAPIEnabled():
        q = text
        salt = random.randint(32768, 65536)

        sign = appid + q + str(salt) + secretKey
        md5s = hashlib.md5()
        md5s.update(sign)
        data = {
            'appid': appid,
            'q': text,
            'from': 'auto',
            'to': 'zh',
            'salt': salt,
            'sign': md5s.hexdigest()
        }
        url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
        res = requests.get(url=url, timeout=2, params=data)
        if res.ok:
            return json.loads(res.text)["trans_result"][0]['dst']
        else:
            derror('error')
    else:
        trans = Moemi()
        result = trans.jp2zh(text)
        return result
        

if __name__ == "__main__":
    s = u"瑞希「希さんのおかげでぽかしてます」"
    t = translate(s, to='sv', fr='ja')
    print t

# EOF
