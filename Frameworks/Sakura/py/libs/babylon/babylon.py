# coding: utf8
# 7/21/2019 mines
#
# See https://fanyi.qq.com/

if __name__ == '__main__':
  import sys
  sys.path.append('..')

import requests
import re
import json
import time
from sakurakit.skdebug import dwarn, derror

def translate(text, to='zhs', fr='ja'):
  session = requests.session()
  url = 'https://fanyi.qq.com/'
  headers = {'Connection': 'keep-alive',
             'Accept': '*/*',
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
             'Content-Type': 'charset=UTF-8',
             'Accept-Encoding': 'gzip, deflate, br'}
  try:
    html1 = session.get(url=url, headers=headers)
    if html1.ok:
      htmlc = html1.content.decode("utf-8")
      qtv = re.findall(r"var qtv = \"(.*?)\";", htmlc, re.S)[0]
      qtk = re.findall(r"var qtk = \"(.*?)\";", htmlc, re.S)[0]
      url = 'https://fanyi.qq.com/api/translate'
      headers = {'Host': 'fanyi.qq.com',
                 'Connection': 'keep-alive',
                 'Accept': 'application/json, text/javascript, */*',
                 'Origin': 'https://fanyi.qq.com',
                 'X-Requested-With': 'XMLHttpRequest',
                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
                 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                 'Referer': 'https://fanyi.qq.com/',
                 'Accept-Encoding': 'gzip, deflate, br'}
      postData = {"source": "jp",
                  "target": "zh",
                  "sourceText": text,
                  "qtv": qtv,
                  "qtk": qtk,
                  "sessionUuid": 'translate_uuid' + str(time.time() * 1000).split('.')[0]}
      html2 = session.post(url=url, data=postData, headers=headers)
      if html2.ok:
        con = ''
        for strs in json.loads(html2.content)["translate"]["records"]:
          con += strs["targetText"]
        return con
      else:
          derror('error')
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