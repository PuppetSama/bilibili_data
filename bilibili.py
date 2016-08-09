# -*- coding:utf-8 -*-
#import urllib
#from urllib.request import *


#url = 'http://www.bilibili.com'
#try:
#    request = Request(url)
#    response = urlopen(request)
#    print(response.read())
#except(urllib2.URLError, e):
#	if hasattr(e,"code"):
#        print(e.code)
#    if hasattr(e,"reason"):
#        print(e.reason)

import urllib.request
import gzip

def getUrlContent(url):  
    #返回页面内容  
    doc = urllib.request.urlopen(url).read()  
    #解码  
    try:  
        html=gzip.decompress(doc).decode("utf-8")  
    except:  
        html=doc.decode("utf-8")  
    return html  

rage = 1
url = "http://www.bilibili.com/video/douga-mad-1.html"
#data = urllib.request.urlopen(url).read()
data =getUrlContent(url)
#buf = StringIO.StringIO(<response object>.content)
#gzip_f = gzip.GzipFile(fileobj=buf)
#content = gzip_f.read()

#data = data.decode('utf-8')
print(data)