# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
import re
import mysql.connector

aid = 9
conn = mysql.connector.connect(
    user='root',
    password='Kang',
    database='bilibili')
cur = conn.cursor()
headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}##浏览器请求头（大部分网站没有这个请求头会报错、请务必加上哦）

def url_data(aid):
    all_url = 'https://www.bilibili.com/video/av' + str(aid)  ##开始的URL地址
    start_html = requests.get(all_url,  headers=headers)  ##使用requests中的get方法来获取all_url的内容 headers为上面设置的请求头、请务必参考requests官方文档解释
    pattern = re.compile('<script type=\'text/javascript\'>.*?cid=(.*?)&aid=.*?&.*?</script>', re.S)
    items = re.findall(pattern, start_html.text)
    if items is None:
            pattern = re.compile('<iframe.*?class=\"player\".*?cid=(.*?)&aid=.*?\"', re.S)
            items = re.findall(pattern, start_html.text)
    for item in items:
        return item

def print_data(item):
    data_url =  'https://interface.bilibili.com/player?id=cid:' + str(item) + '&aid=' + str(aid)
    data_html = requests.get(data_url,  headers=headers) 
    Soup = BeautifulSoup(data_html.text, 'lxml')
    print aid
    data_typeid = Soup.find('typeid')
    for typeid in data_typeid: print typeid
    data_click = Soup.find('click')
    for click in data_click: print click
    data_fa = Soup.find('favourites')
    for favourites in data_fa: print favourites
    data_coins = Soup.find('coins')
    for coins in data_coins: print coins

    query = ("insert into bili_data(aid, typeid, click, favourites, coins) values('%s','%s','%s','%s','%s') " %(aid, typeid, click, favourites, coins))
    cur.execute(query) 
    conn.commit()

while 1:
    item = url_data(aid)
    if item:
        print_data(item)
    else:
        print '未能找到有效信息'
    aid+=1
