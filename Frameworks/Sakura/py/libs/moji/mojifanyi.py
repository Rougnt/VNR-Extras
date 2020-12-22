# coding: utf8
# k1mlka
import requests
import json
import settings

installtion_id = settings.global_().getMojiID()
session_token = settings.global_().getMojiToken()

def translate(text, to='zhs', fr='ja'):
    url = 'https://www.mojidict.com/'
    api_url = 'https://api.mojidict.com/parse/functions/multiTrans'
    try:
        if settings.global_().isMojiAPIEnabled():
            head = {
                "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36" 
            }

            payload = {
                'text': text, 
                '_ApplicationId': 'E62VyFVLMiW7kvbtVq3p', 
                '_ClientVersion': 'js2.10.0', 
                '_InstallationId': installtion_id, 
                '_SessionToken': session_token
            }

            s = requests.Session()
            s.headers.update(head)

            r = s.post(api_url, json=payload)
            trans = json.loads(r.content)["result"]["trans_dst"]
            return trans

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
