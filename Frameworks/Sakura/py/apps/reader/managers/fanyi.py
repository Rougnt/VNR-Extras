# coding: utf8

import jpype
from jpype import *
import os
import settings

path = os.path.abspath(__file__)
pos = path.rfind('Sakura')
jvm = path[0:pos] + 'jre\\bin\\client\\jvm.dll'
imp = path[0:pos+6] + '\\jar\\tran.jar'
jar = path[0:pos+6] + '\\jar'
jpype.startJVM(jvm, "-ea", "-Djava.class.path=%s" %imp, "-Djava.ext.dirs=%s" %jar)
JClass = jpype.JClass('fan.Fanyi')

baidu_id = settings.global_().getBaiduAppID()
baidu_key = settings.global_().getBaiduKey()
tengxun_id = settings.global_().getTengxunAppID()
tengxun_key = settings.global_().getTengxunKey()

def translate(s, b1, b2, b3, b4):    
    # baidu tengxun youdao caiyun
    b5 = b1 & settings.global_().isBaiduAPIEnabled()
    b6 = b2 & settings.global_().isTengxunAPIEnabled()
    if b5 | b6:
        return JClass.translate(s, baidu_id if b5 else "", baidu_key if b5 else "",
                                tengxun_id if b6 else "", tengxun_key if b6 else "", b3, b4)
    else:
        return JClass.translate(s, "t" if b1 else "", "", "t" if b2 else "", "", b3, b4)

if __name__ == "__main__":
    s = u"いつまでもいつまでも越えられない夜を，超えようと手をつなぐこの日々が続きますように。"
    t = translate(s, True, True, True, True)
    print t




