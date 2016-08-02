# -*- coding:utf-8 -*-
import urllib
from urllib.request import *


#page = 1
url = 'http://www.bilibili.com'
try:
    request = Request(url)
    response = urlopen(request)
    print(response.read())
except(urllib2.URLError, e):
    if hasattr(e,"code"):
        print(e.code)
    if hasattr(e,"reason"):
        print(e.reason)