# coding: utf8
# bingman.py
# 10/7/2014 jichi
# 1/21/2018 tinyAdapter

from sakurakit.skclass import memoized
from sakurakit import skthreads
from microsoft import bingauth, bingtrans, bingtts

@memoized
def manager(): return BingManager()

class BingManager:

  def __init__(self):
    self.__d = _BingManager()
    self.__t = bingtrans.BingHtmlTranslator()

  def translate(self, *args, **kwargs): # -> unicode  text
    #appId = self.__d.appId()
    return self.__t.translate(*args, **kwargs)

  def tts(self, *args, **kwargs): # -> unicode  url
    appId = self.__d.appId()
    return bingtts.url(*args, **kwargs)

class _BingManager:
  def __init__(self):
    self._appId = None

  def appId(self):
    """
    @return  str or None
    """
    return None

# EOF
