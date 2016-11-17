# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
import time
import re
import mysql.connector

aid = 1
headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}

def url_data(aid):    
    all_url = 'https://www.bilibili.com/video/av' + str(aid)
    start_html = requests.get(all_url,  headers=headers)
    pattern = re.compile('<script type=\'text/javascript\'>.*?cid=(.*?)&aid=.*?&.*?</script>', re.S)
    items = re.findall(pattern, start_html.text)
    if not bool(items):
        pattern = re.compile('<iframe.*?class=\"player\".*?cid=(.*?)&aid=.*?\"', re.S)
        items = re.findall(pattern, start_html.text)
    for item in items:
        return item
    s = requests.session()
    s.keep_alive = False

def print_data(item):

    conn = mysql.connector.connect(
    user='root',
    password='Kang',
    database='bilibili')
    cur = conn.cursor()
    print aid
    data_url =  'https://interface.bilibili.com/player?id=cid:' + str(item) + '&aid=' + str(aid)
    data_html = requests.get(data_url, headers=headers, timeout = 10) 
    Soup = BeautifulSoup(data_html.text, 'lxml')
    typeid = Soup.typeid.get_text()
    click = Soup.click.get_text()
    favourites = Soup.favourites.get_text()
    coins = Soup.coins.get_text()

    query = ("insert into bili_data(aid, typeid, click, favourites, coins) values('%s','%s','%s','%s','%s') " %(aid, typeid, click, favourites, coins))
    cur.execute(query) 
    conn.commit()
    conn.close()

while 1:
    item = url_data(aid)
    time.sleep(0.5)
    if item:
        print_data(item)
    else:
        print 'None'
    aid+=1
