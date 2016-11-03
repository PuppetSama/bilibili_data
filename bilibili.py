# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
import re

headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}##浏览器请求头（大部分网站没有这个请求头会报错、请务必加上哦）
all_url = 'https://www.bilibili.com/video/av9'  ##开始的URL地址
start_html = requests.get(all_url,  headers=headers)  ##使用requests中的get方法来获取all_url的内容 headers为上面设置的请求头、请务必参考requests官方文档解释
#print(start_html.text) ##打印出start_html (请注意，concent是二进制的数据，一般用于下载图片、视频、音频、等多媒体内容是才使用concent, 对于打印网页内容请使用text)

pattern = re.compile('<script type=\'text/javascript\'>.*?cid=(.*?)&aid=.*?&.*?</script>', re.S)
items = re.findall(pattern, start_html.text)
if items == []:
        pattern = re.compile('<iframe.*?class=\"player\".*?cid=(.*?)&aid=.*?\"', re.S)
        items = re.findall(pattern, start_html.text)
for item in items:
    item

data_url =  'https://interface.bilibili.com/player?id=cid:' + str(item) + '&aid=9'
data_html = requests.get(data_url,  headers=headers) 
Soup = BeautifulSoup(data_html.text, 'lxml')
data_click = Soup.find('click')
for click in data_click: print click
data_fa = Soup.find('favourites')
for favourites in data_fa: print favourites
data_coins = Soup.find('coins')
for coins in data_coins: print coins
data_typeid = Soup.find('typeid')
for typeid in data_typeid: print typeid
