# coding: UTF-8
# Tencent Translate Interface
# Author: Shiroha
# Version: 1.0
# Date: 2019-07-19


import requests
import re
import time
import json

session = None

class TTI:
  def __init__(self):
    self.url = 'https://fanyi.qq.com'
    self.api = 'https://fanyi.qq.com/api/translate'
    self.fail_time = 0.0
    self.qtv = None
    self.qtk = None
    # for cookies
    self.session = requests.Session()

  def get_token(self):
    try:
      resp = self.session.get(self.url)
      # find qtv
      result = re.findall('qtv = "(.+?)"', resp.content)
      self.qtv = result[0]
      # find qtk
      result = re.findall('qtk = "(.+?)"', resp.content)
      self.qtk = result[0]
    except:
      raise

  def init_token(self):
    # load
    if not self.qtv or not self.qtk:
      self.get_token()
      self.get_token()
    # check
    if not self.qtv or not self.qtk:
      raise Exception('load token failed')

  def reset_session(self):
    self.session = requests.Session()
    self.qtv = None
    self.qtk = None

  def translate(self, fr, to, text):
    # check reset
    if self.fail_time > 0.0:
      if time.clock() - self.fail_time < 50.0:
        print('tencent failure trying to reset')
        return ''
      else:
        self.fail_time = 0.0
        self.reset_session()
    # init token
    try:
      self.init_token()
    except:
      raise
    # Request Headers
    headers = {
      'Accept': 'application/json, text/javascript, */*; q=0.01',
      'Accept-Encoding': 'gzip, deflate, br',
      'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
      'Connection': 'keep-alive',
      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      'Host': 'fanyi.qq.com',
      'Origin': 'https://fanyi.qq.com',
      'Referer': 'https://fanyi.qq.com/',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
      'X-Requested-With': 'XMLHttpRequest'
    }
    # Form Data
    data = {
      'source': 'jp',
      'target': 'zh',
      'sourceText': text,
      'qtv': self.qtv,
      'qtk': self.qtk,
      'sessionUuid': 'translate_uuid' + str(int(time.time() * 1000.0))
    }
    # Submit
    try:
      resp = self.session.post(self.api, data=data, headers=headers)
      if resp.ok:
        j = json.loads(resp.content)
        if j['errCode'] == 0:
          t = j['translate']
          if t['errCode'] == 0:
            r = t['records']
            if len(r) > 0:
              s = ''
              for e in r:
                d = e['targetText']
                if d[0] != '{':
                  s += d
              return s
          else:
            self.fail_time = time.clock()
            print('tencent error trying to reset')
            return ''
        else:
          self.fail_time = time.clock()
          print('tencent error trying to reset')
          return ''
      elif resp.status_code == 401 or resp.status_code == 403:
        # try to reset
        self.fail_time = time.clock()
        print('tencent status code %d trying to reset' % resp.status_code)
        return ''
      else:
        raise Exception('translate failed %d' % resp.status_code)
    except:
      raise

tti = TTI()

def translate(text, to='zhs', fr='ja', align=None):
  try:
    return tti.translate(fr, to, text)
  except Exception as e:
    raise Exception('translate failed -> ' + e.message)

# TEST CODE

if __name__ == "__main__":
  print(tti.translate('jp', 'zh', "日曜か。特に予定はないけど、どうかしたか？"))
  print(tti.translate('jp', 'zh', "うむ。実はお前を水族館に連れてってやろうと思ってな"))
  print(tti.translate('jp', 'zh', "水族館？"))
