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
import base64
import hashlib
import hmac
import settings
from sakurakit.skdebug import dwarn, derror

qtv = ""
qtk = ""
tengxun_id = settings.global_().getTengxunAppID()
tengxun_key = settings.global_().getTengxunKey()

def get_string_to_sign(method, endpoint, params):
    s = method + endpoint + "/?"
    query_str = "&".join("%s=%s" % (k, params[k]) for k in sorted(params))
    return s + query_str

def sign_str(key, s, method):
    hmac_str = hmac.new(key.encode("utf8"), s.encode("utf8"), method).digest()
    return base64.b64encode(hmac_str)

def get_qt_code():
    session = requests.session()
    global qtv
    global qtk
    url = 'https://fanyi.qq.com/'
    headers = {'Connection': 'keep-alive',
               'Accept': '*/*',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
               'Content-Type': 'charset=UTF-8',
               'Accept-Encoding': 'gzip, deflate, br'}
    html1 = session.get(url=url, headers=headers, timeout=2)
    if html1.ok:
        htmlc = html1.content.decode("utf-8")
        qtv = re.findall(r"var qtv = \"(.*?)\";", htmlc, re.S)[0]
        qtk = re.findall(r"var qtk = \"(.*?)\";", htmlc, re.S)[0]
    else:
        derror('error')


def translate(text, to='zhs', fr='ja'):
    try:
        session = requests.session()
        if settings.global_().isTengxunAPIEnabled():
            endpoint = "tmt.tencentcloudapi.com"
            data = {
                'Action': 'TextTranslate',
                'Nonce': 11186,
                'ProjectId': '0',
                'Region': 'ap-guangzhou',
                'SecretId': tengxun_id,
                'Source': 'auto',
                'SourceText': text,
                'Target': 'zh',
                'Timestamp': int(time.time()),
                'Version': '2018-03-21'
            }
            s = get_string_to_sign("GET", endpoint, data)
            data["Signature"] = sign_str(tengxun_key, s, hashlib.sha1)
            # 此处会实际调用，成功后可能产生计费
            resp = session.get(url="https://" + endpoint, params=data)
            return json.loads(resp.content)["Response"]["TargetText"]
        else:
            session = requests.session()
            if len(qtv) == 0:
                get_qt_code()
            url = 'https://fanyi.qq.com/api/translate'
            headers = {'Host': 'fanyi.qq.com',
                       'Connection': 'keep-alive',
                       'Accept': 'application/json, text/javascript, */*',
                       'Origin': 'https://fanyi.qq.com',
                       'X-Requested-With': 'XMLHttpRequest',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                     'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
                       'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                       'Referer': 'https://fanyi.qq.com/',
                       'Accept-Encoding': 'gzip, deflate, br'}
            data = {"source": "jp",
                    "target": "zh",
                    "sourceText": text,
                    "qtv": qtv,
                    "qtk": qtk,
                    "sessionUuid": 'translate_uuid' + str(time.time() * 1000).split('.')[0]}

            html2 = session.post(url=url, data=data, headers=headers, timeout=2)
            if html2.ok:
                con = ''
                for strs in json.loads(html2.content)["translate"]["records"]:
                    con += strs["targetText"]
                if con.encode("utf-8") == "。" or con.encode("utf-8") == "":
                    get_qt_code()
                    con = translate(text)
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
    else:
        pass


if __name__ == "__main__":
    s = u"竜が，俺の敌を喰らえ！竜神の剣を喰らえ！"
    t = translate(s, to='sv', fr='ja')
    print t
