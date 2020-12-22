# coding: utf8
# 7/21/2019 mines
#
# See: http://shared.ydstatic.com/fanyi/newweb/v1.0.19/scripts/newweb/fanyi.min.js

if __name__ == '__main__':
  import sys
  sys.path.append('..')

import requests
import json
import time
import hashlib
from sakurakit.skdebug import dwarn, derror

cookies = ''

def get_cookie():
    global cookies
    session = requests.session()
    url = 'http://fanyi.youdao.com/'
    headers = {'Connection': 'keep-alive',
               'Accept': '*/*',
               "Accept-Language": "zh-CN",
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
               'Content-Type': 'charset=UTF-8',
               'Accept-Encoding': 'gzip, deflate, br'}
    html1 = session.get(url=url, headers=headers, timeout=2)
    if html1.ok:
        dict = requests.utils.dict_from_cookiejar(html1.cookies)
        for cookie in dict:
            cookies += cookie + '=' + dict[cookie] + ';'
    else:
        derror("error")

def translate(text, to='zhs', fr='ja'):
  if cookies == '':
      get_cookie()
  session = requests.session()
  try:
      ts = str(time.time() * 1000).split('.')[0]
      salt = str(int(ts) / 10).split('.')[0]
      md5s = hashlib.md5()
      md5s.update(("fanyideskweb" + text + salt + "n%A-rKaT5fb[Gy?;N5@Tj").encode('utf-8'))
      url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
      headers = {'Host': 'fanyi.youdao.com',
                 'Connection': 'keep-alive',
                 'Accept': 'application/json, text/javascript, */*',
                 'Origin': 'https://fanyi.qq.com',
                 'X-Requested-With': 'XMLHttpRequest',
                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
                 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                 'Cookie': cookies,
                 'Referer': 'http://fanyi.youdao.com/',
                 'Accept-Encoding': 'gzip, deflate'}
      postData = {"from": "ja",
                  "to": "zh-CHS",
                  "smartresult": "dict",
                  "client": "fanyideskweb",
                  "ts": ts,
                  "bv": "53539dde41bde18f4a71bb075fcf2e66",
                  "salt": salt,
                  "sign": md5s.hexdigest(),
                  "i": text,
                  "doctype": "json",
                  "version": "2.1",
                  "keyfrom": "fanyi.web",
                  "action": "FY_BY_CLICKBUTTION"}
      html2 = session.post(url=url, data=postData, headers=headers, timeout=2)
      if html2.ok:
          con = ''
          for strs in json.loads(html2.content)["translateResult"][0]:
              con += strs["tgt"]
          return con
      else:
          derror('error')

  except requests.ConnectionError, e:
    dwarn("connection error", e.args)
  except requests.HTTPError, e:
    dwarn("http error", e.args)
  except UnicodeDecodeError, e:
    dwarn("unicode decode error", e)
  except (ValueError, KeyError, IndexError, TypeError), e:
    dwarn("json format error", e)
  except Exception, e:
    derror('error', e)
  else: pass

if __name__ == "__main__":
    s = u"竜が，俺の敌を喰らえ！竜神の剣を喰らえ！"
    t = translate(s, to='sv', fr='ja')
    print t


