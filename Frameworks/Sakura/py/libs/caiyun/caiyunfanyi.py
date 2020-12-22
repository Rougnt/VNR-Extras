# coding: utf8
# 8/4/2019 mines
#
# See https://fanyi.caiyunapp.com/#/

if __name__ == '__main__':
    import sys
    import os
    lib_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    sys.path.append(lib_path)

import requests
import re
import json
import time
from sakurakit.skdebug import dwarn, derror
import settings

token_id = settings.global_().getCaiyunToken()

def translate(text, to='zhs', fr='ja'):
    session = requests.session()
    try:
        # this is free test token in api document
        token = "token 3975l6lr5pcbvidl6jl2"
        if settings.global_().isCaiyunAPIEnabled():
            token = "token " + token_id
        url = 'http://api.interpreter.caiyunai.com/v1/translator'
        headers = {'x-authorization': token,
                   'Content-Type': 'application/json;charset=UTF-8',}
        data = {"source": text,
                "trans_type": "auto2zh",
                "request_id": "demo",
                "detect": True,}
        html2 = session.post(url=url, data=json.dumps(data), headers=headers, timeout=2)
        if html2.ok:
            return json.loads(html2.content)["target"]
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
