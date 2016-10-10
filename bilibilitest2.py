# -*- coding:utf-8 -*-
import urllib
import urllib2
import gzip
import re
import StringIO

i = 13959
k = 0
def url_data(page):
    url = 'https://www.bilibili.com/video/av' + str(page)
    try:
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        if response.info().get('Content-Encoding') == 'gzip':
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

    pattern = re.compile('<iframe.*?class=\"player\".*?cid=(.*?)&aid=(.*?)\"', re.S)
    items = re.findall(pattern, content)

    return items,content



def print_data():
    pageDatas = []
    for item in items:
        print item[0],item[1]
    title_pattern = re.compile('<title>(.*?)</title>', re.S)
    title_item = re.findall(title_pattern, content)[0]
    title_items = title_item.split('_')
    time_pattern = re.compile('<time itemprop="startDate".*?<i>(.*?)</i></time>', re.S)
    time_item = re.findall(time_pattern, content)[0]
    intro_pattern = re.compile('<div id="v_desc">(.*?)</div>', re.S)
    if re.findall(intro_pattern, content):
        intro_item = re.findall(intro_pattern, content)[0]
    else:
        intro_item = None
    usname_pattern = re.compile('class="name".*?title="(.*?)"', re.S)
    if re.findall(usname_pattern, content):
        usname_item = re.findall(usname_pattern, content)[0]
    else:
        usname_item = None
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

    pageDatas.append(['av' + item[1],title_items[0],title_items[2],title_items[1],time_item,usname_item,intro_item,click_item,fa_item,coins_item])

    for data in pageDatas:
        targetData = "\n视频号:%s\t视频名称:%s\t分类:%s>%s\t投稿时间:%s\tup主:%s\n视频说明:%s\n播放量:%s\t收藏量:%s\t硬币数:%s\n" %(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9])
        f = open('bilibili.html', 'a')
        f.write(targetData)
        f.close()
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
while 1:
    items,content = url_data(i)
    i+=1
    k+=1
    if len(items):
        print_data()
    else:
        print '未能找到有效信息'

print k




#    buf = StringIO.StringIO( response.read())
#    gzip_f = gzip.GzipFile(fileobj=buf)
#    content = gzip_f.read()
#else:
#    content = response.read().decode('utf-8')


# urllib2.URLError: <urlopen error [Errno 10060] > 
# 一场url输入不正确引发的血案

# UnicodeDecodeError: 'ascii' codec can't decode byte 0x8b in position 1: ordinal not in range(128)
# gzip The server sends gzipped stream.
# 对于无法正确匹配信息的部分，主要有两类：1，网站代码和后期不同，目前实例仅有av1
# 2，视频不存在
# 检测items是否为空，即能否取到aid及cid，不能则认为其不存在