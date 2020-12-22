# coding: utf8
# googletrans.py
# 8/2/2013 jichi

if __name__ == '__main__':
  import sys
  sys.path.append('..')

__all__ = 'GoogleTranslator', 'GoogleHtmlTranslator', 'GoogleJsonTranslator'

import requests
from sakurakit import sknetdef
from sakurakit.skdebug import dwarn, derror
from sakurakit.skstr import unescapehtml
import googledef
import math
import re
import requests
import time


FANYI_TKK = ""
FANYI_Time = 0
FANYI_Hour = 0
TimeSpan = 1800
session = requests


def getTKK(text):
    r = re.search(r'tkk:[\S](\d+\.\d+)', text, re.M|re.S)
    if r:
        return r.group(1)
    else:
        return ""


def getSource():
    req = session.get("https://translate.google.cn")
    if req.ok:
        return req.content
    else:
        return ""


def checkTime():
    global FANYI_Time
    global FANYI_Hour
    global FANYI_TKK
    t = time.time()
    h = time.localtime(t).tm_hour
    istrue = t - FANYI_Time > TimeSpan or h != FANYI_Hour or FANYI_TKK == ""
    if istrue:
        FANYI_Time = t
        FANYI_Hour = h
        dwarn("check tkk", FANYI_TKK)
    return istrue


def tryUpdataTkk():
    global FANYI_TKK
    if checkTime():
        source = getSource()
        if source != "":
            tkk = getTKK(source)
            dwarn("updata tkk", tkk)
            if tkk != "" and tkk != FANYI_TKK:
                FANYI_TKK = tkk


def orz(x, y):
    for t in range(0, len(y) -2, 3): 
        a = y[t + 2]
        if a >= 'a':
            a = ord(a[0]) -87
        else:
            a = int(a)
        if '+' == y[t + 1]:
            a = (x >> a) & int("11111111111111111111111111111111"[a:], 2)
        else:
            a = x << a
        if '+' == y[t]:
            x = x + a & 4294967295
        else:
            x = x ^ a
    return x


def getSign(a):
    d = FANYI_TKK.split('.')
    z = int(d[0]) or 0
    s = int(d[1]) or 0
    S = []
    c = 0
    for v in range(0, len(a), 1):
        A = ord(a[v])
        if 128 > A:
            S.append(A)
        else:
            if 2048 > A :
                S.append(A >> 6 | 192)
            else:
                if (55296 == (64512 & A) and (v + 1) < len(a) and 56320 == (64512 & ord(a[v + 1]))):
                    A = 65536 + ((1023 & A) << 10) + (1023 & ord(a[++v]))
                    S.append(A >> 18 | 240)
                    S.append(A >> 12 & 63 | 128)
                else:
                    S.append(A >> 12 | 224)
                    S.append(A >> 6 & 63 | 128)
            S.append(63 & A | 128)
    p = z
    for b in range(0, len(S), 1):
        p += S[b]
        p = orz(p, '+-a^+6')
    p = orz(p, '+-3^+b+-f')
    p ^= s
    if 0 > p:
         p = (2147483647 & p) + 2147483648
    p %= 1000000
    return str(p) + '.' + str(p ^ z)


# https://translate.google.cn/translate_a/single?client=webapp&sl=ja&tl=zh-CN&hl=zh-CN&dt=t&tk=876620.785187&q=
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0
# Host: translate.google.cn


def u_translate(text, to='zhs', fr='ja', session = requests):
  try:
    tryUpdataTkk()
    if FANYI_TKK == "":
        return u"获取tkk错误"
    api = 'https://translate.google.cn/translate_a/single'
    sign = getSign(text)
    dwarn("get sign f tkk", FANYI_TKK)
    u_params = {
        'client':'webapp',
        'sl':'ja',
        'tl':'zh-CN',
        'hl':'zh-CN',
        'dt':'t',
        'tk':sign,
        'q':text
    }
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Host': 'translate.google.cn'
    }

    r = session.get(api,
        headers = headers,
        params = u_params
    )
    ret = r.content
    if r.ok and len(ret) > 10:
        r = re.search(r'"([^"]+)', ret, re.M|re.S)
        if r:
            return r.group(1)
    return ret

  except requests.ConnectionError, e:
    dwarn("connection error", e.args)
  except requests.HTTPError, e:
    dwarn("http error", e.args)
  except UnicodeDecodeError, e:
    dwarn("unicode decode error", e)
  except (ValueError, IndexError), e:
    dwarn("text format error", e)
  except Exception, e:
    dwarn("baidu-error", e)
  else:
    return "error"

# Remove repetive comma only before "or[ and after "or].
_re_gson_comma = re.compile(r'(?<=[\]"],),+(?=[\["])')
def eval_gson_list(data): pass
class GoogleTranslator(object): pass

class GoogleHtmlTranslator(GoogleTranslator):
  session = requests
  def translate(self, t, to='auto', fr='auto'): 
    return u_translate(t, 'zhs', 'ja', session)


class GoogleJsonTranslator(GoogleTranslator):
  session = requests
  def translate(self, t, to='auto', fr='auto', align=None): 
    return u_translate(t, 'zhs', 'ja', session)
  def _iteralign(self, data): pass
  def analyze(self, t, to='auto', fr='auto', align=None): pass


if __name__ == '__main__':
  s = u"本田"
  t = translate(s, to='zhs', fr='ja')
  #t = translate(u"神楽", to='zhs', fr='ja')
  print t

# EOF
