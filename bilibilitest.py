# -*- coding:utf-8 -*-
import urllib
import urllib2
import gzip
import re
import StringIO

page = 5976904
url = 'https://www.bilibili.com/video/av' + str(page)
try:
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    if response.info().get('Content-Encoding') == 'gzip':
        # request.add_header('Accept-encoding', 'gzip')
        # opener = urllib2.build_opener()
        # f = opener.open(request)
        # compresseddata = f.read()
        # compressedstream = StringIO.StringIO(compresseddata)
        # gzipper = gzip.GzipFile(fileobj=compressedstream)
        # print gzipper.read()
        buf = StringIO.StringIO( response.read())
        gzip_f = gzip.GzipFile(fileobj=buf)
        content = gzip_f.read()
    else:
        content = response.read().decode('utf-8')
except urllib2.URLError, e:
	if hasattr(e, "code"):
		print e.code
	if hasattr(e, "reason"):
		print e.reason

# 拉出来看看是否有需要的信息
#f = open('bilibili.html', 'w')
#f.write(content)
#f.close()

#pattern = re.compile('<script type=\'text/javascript\'>EmbedPlayer(\'player\', \"http://static.hdslb.com/play.swf\", \"cid=(.*?)&aid=(.*?)&pre_ad=0\");</script>', re.S)
pattern = re.compile('<script type=\'text/javascript\'>.*?cid=(.*?)&aid=(.*?)&.*?</script>', re.S)
items = re.findall(pattern, content)
print items
for item in items:
	print item[0],item[1]
title_pattern = re.compile('<title>(.*?)</title>', re.S)
title_item = re.findall(title_pattern, content)[0]
title_items = title_item.split('_')
time_pattern = re.compile('<time itemprop="startDate".*?<i>(.*?)</i></time>', re.S)
time_item = re.findall(time_pattern, content)[0]
intro_pattern = re.compile('<div id="v_desc">(.*?)</div>', re.S)
intro_item = re.findall(intro_pattern, content)[0]
usname_pattern = re.compile('class="name".*?title="(.*?)"', re.S)
usname_item = re.findall(usname_pattern, content)[0]
print 'av' + item[1],title_items[0],'分类',title_items[2],title_items[1]
print '投稿时间',time_item,'up主',usname_item
print '视频说明'
print intro_item

dataUrl = 'https://interface.bilibili.com/player?id=cid:' + str(item[0]) + '&aid=' + str(item[1])
dataRequest = urllib2.Request(dataUrl)
dataResponse = urllib2.urlopen(dataRequest)
#if dataResponse.info().get('Content-Encoding') == 'gzip':
dataRequest.add_header('Accept-encoding', 'gzip')
opener = urllib2.build_opener()
f = opener.open(dataRequest)
compresseddata = f.read()
compressedstream = StringIO.StringIO(compresseddata)
gzipper = gzip.GzipFile(fileobj=compressedstream)
dataContent = gzipper.read()
click_pattern = re.compile('<click>(.*?)</click>',re.S)
click_item = re.findall(click_pattern, dataContent)[0]
fa_pattern = re.compile('<favourites>(.*?)</favourites>',re.S)
fa_item = re.findall(fa_pattern, dataContent)[0]
coins_pattern = re.compile('<coins>(.*?)</coins>',re.S)
coins_item = re.findall(coins_pattern, dataContent)[0]

print '播放量',click_item,'收藏量',fa_item,'硬币数',coins_item
#    buf = StringIO.StringIO( response.read())
#    gzip_f = gzip.GzipFile(fileobj=buf)
#    content = gzip_f.read()
#else:
#    content = response.read().decode('utf-8')


# urllib2.URLError: <urlopen error [Errno 10060] > 
# 一场url输入不正确引发的血案

# UnicodeDecodeError: 'ascii' codec can't decode byte 0x8b in position 1: ordinal not in range(128)
# gzip The server sends gzipped stream.