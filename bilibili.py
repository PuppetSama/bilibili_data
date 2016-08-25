# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import httplib
import StringIO
import gzip

page = 111
url = 'https://www.bilibili.com/video/av' + str(page)
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }
try:
    request = urllib2.Request(url,headers = headers)
    try:
        request.add_header('Accept-encoding', 'gzip')
        opener = urllib2.build_opener()
        f = opener.open(request)
        compresseddata = f.read()
        compressedstream = StringIO.StringIO(compresseddata)
        gzipper = gzip.GzipFile(fileobj=compressedstream)
        print gzipper.read()
    except IOError, e:
        response = urllib2.urlopen(request)
        content = response.read().decode('utf-8')
        pattern = re.compile('<script type=\'(.*?)/javascript\'>', re.S)
        items = re.findall(pattern, content)
        for item in items:
    	    print item[0].encode('utf-8')
    	    print '--------------------'
    	    #print item[1].encode('utf-8')
        #print response.read()
except urllib2.URLError, e:
    if hasattr(e,"code"):
        print e.code
    if hasattr(e,"reason"):
        print e.reason