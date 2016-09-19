# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import StringIO
import gzip

#bilibili爬虫类
class Bilibili(object):
    """docstring for Bilibili"""
    #初始化方法，定义变量
    def __init__(self):
        #起始av号
        self.pageIndex = 1111
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = { 'User-Agent' : self.user_agent }
        #存放数据的变量
        self.datas = []
        #判断程序是否运行
        self.enable = False
    #传入索引值获取页面代码
    def getPage(self, pageIndex):
        try:
            url = 'https://www.bilibili.com/video/av' + str(pageIndex)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            if response.info().get('Content-Encoding') == 'gzip':
                buf = StringIO.StringIO( response.read())
                gzip_f = gzip.GzipFile(fileobj=buf)
                content = gzip_f.read()
            else:
                content = response.read().decode('utf-8')
            return content
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason
            return None

    #传入页面代码，返回所需信息
    def getPageItems(self, pageIndex):
        content = self.getPage(pageIndex)
        if not content:
            print '页面加载失败'
            return None
        pattern = re.compile('<script type=\'text/javascript\'>.*?cid=(.*?)&aid=(.*?)&.*?</script>', re.S)
        items = re.findall(pattern, content)
        pageDatas = []
        if not len(items):
            print '未能找到有效信息|该视频不存在'
            return None
        for item in items:
            item[0],item[1]
        title_pattern = re.compile('<title>(.*?)</title>', re.S)
        title_item = re.findall(title_pattern, content)[0]
        title_items = title_item.split('_')
        time_pattern = re.compile('<time itemprop="startDate".*?<i>(.*?)</i></time>', re.S)
        time_item = re.findall(time_pattern, content)[0]
        intro_pattern = re.compile('<div id="v_desc">(.*?)</div>', re.S)
        intro_item = re.findall(intro_pattern, content)[0]
        usname_pattern = re.compile('class="name".*?title="(.*?)"', re.S)
        usname_item = re.findall(usname_pattern, content)[0]
        #print 'av' + item[1],title_items[0],'分类',title_items[2],title_items[1]
        #print '投稿时间',time_item,'up主',usname_item
        #print '视频说明'
        #print intro_item

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

        #print '播放量',click_item,'收藏量',fa_item,'硬币数',coins_item

        pageDatas.append(['av' + item[1],title_items[0],title_items[2],title_items[1],time_item,usname_item,intro_item,click_item,fa_item,coins_item])

        return pageDatas

    #获取一个视频信息
    def getOneAv(self,pageDatas,pageIndex):
        for data in pageDatas:
            input = raw_input()
            pageDatas = self.getPageItems(self.pageIndex)
            if pageDatas:
                self.datas.append(pageDatas)
                self.pageIndex += 1
            if input == 'Q':
                self.enable = False
                return
            print "视频号:%s\t视频名称:%s\t分类:%s>%s\t投稿时间:%s\tup主:%s\n视频说明:%s\n播放量:%s\t收藏量:%s\t硬币数:%s" %(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9])

    def start(self):
        self.enable = True
        pageDatas = self.getPageItems(self.pageIndex)
        if pageDatas:
            self.datas.append(pageDatas)
            self.pageIndex += 1
        nowPage = 0
        while self.enable:
            pageDatas = self.datas[0]
            nowPage += 1
            del self.datas[0]
            self.getOneAv(pageDatas,nowPage)

bilibili_spider = Bilibili()
bilibili_spider.start()