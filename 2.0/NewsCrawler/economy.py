import requests 
from lxml import html
from bs4 import BeautifulSoup
from datetime import datetime 
from datetime import timedelta
import sqlite3 as lite
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

requests.packages.urllib3.disable_warnings()

con = lite.connect('../../FBWEB.sqlite')
c = con.cursor()
headers = {'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}


#財經
url = ['https://money.udn.com/rank/newest/1001/12017/1', 'https://money.udn.com/rank/newest/1001/5592/1']
website = '經濟日報'
classification = '財經'
for link in url:
    title = []
    dt = []
    links = []
    view = []
    res = requests.get(link, headers = headers)
    #print(res.text)
    soup = BeautifulSoup(res.text, 'lxml')
#     f = soup.find_all('table')
#    print(f)
    tr = soup.select('tr')[1:]
    #print(list_blocks)
    for value in tr:
        td0 = value.select('td')[0]
        title.append(td0.a.text)
        links.append(td0.a['href'])
        td2 = value.select('td')[2]
        dt.append(td2.text)
        td3 = value.select('td')[3]
        view.append(td3.text)
    today = datetime.today()
    today = datetime.strftime(today,'%m/%d')
#    print(today)
    count = 0
    
    for item in dt:
        if today in item:
            count = count + 1
#            print(count)
    today = datetime.today()
    today = datetime.strftime(today,'%Y/%m/%d')
    for cou in range(0,count):
        res = requests.get(links[cou], headers = headers)
        soup = BeautifulSoup(res.text, 'lxml')
        tr = soup.select('div#story_body p')
        contents = ''
        for t in tr:
            if(len(t.text)>1):
                contents = contents + '\n\n' + t.text.strip()
        c.execute("INSERT INTO News(dt, title, link, website, summary, content, classification) VALUES(?, ?, ?, ?, '', ?, ?)",(today, title[cou], links[cou], website, contents, classification,))
con.commit()


#保險
website = '經濟日報'
classification = '保險'
url = 'https://money.udn.com/search/result/1001/%E4%BF%9D%E9%9A%AA'
title = []
dt = []
links = []
summary = []

res = requests.get(url, headers = headers)
soup = BeautifulSoup(res.text, 'lxml')
tr = soup.select('dt')[70 : 90]

for value in tr:
    links.append(value.a['href'])
    title.append(value.a.h3.text)
    dt.append(value.a.span.text)
    summary.append(value.a.p.text)

today = datetime.today()
today = datetime.strftime(today,'%m/%d')
count = 0
    
for item in dt:
    if today in item:
        count = count + 1     

today = datetime.today()
today = datetime.strftime(today,'%Y/%m/%d')
for cou in range(0,count):
    res = requests.get(links[cou], headers = headers)
    soup = BeautifulSoup(res.text, 'lxml')
    tr = soup.select('div#story_body p')
    contents = ''
    for t in tr:
        if(len(t.text)>1):
            contents = contents + '\n\n' + t.text.strip()
    c.execute("INSERT INTO News(dt, title, link, website, summary, content, classification) VALUES(?, ?, ?, ?, '', ?, ?)",(today, title[cou], links[cou], website, contents, classification,))
con.commit()


#富邦
website = '經濟日報'
classification = '富邦'
url = 'https://money.udn.com/search/result/1001/%E5%AF%8C%E9%82%A6'
title = []
dt = []
links = []
summary = []

res = requests.get(url, headers = headers)
soup = BeautifulSoup(res.text, 'lxml')
tr = soup.select('dt')[70 : 90]

for value in tr:
    links.append(value.a['href'])
    title.append(value.a.h3.text)
    dt.append(value.a.span.text)
    summary.append(value.a.p.text)

today = datetime.today()
today = datetime.strftime(today,'%m/%d')
count = 0
    
for item in dt:
    if today in item:
        count = count + 1

today = datetime.today()
today = datetime.strftime(today,'%Y/%m/%d')
for cou in range(0,count):
    res = requests.get(links[cou], headers = headers)
    soup = BeautifulSoup(res.text, 'lxml')
    tr = soup.select('div#story_body p')
    contents = ''
    for t in tr:
        if(len(t.text)>1):
            contents = contents + '\n\n' + t.text.strip()
    c.execute("INSERT INTO News(dt, title, link, website, summary, content, classification) VALUES(?, ?, ?, ?, '', ?, ?)",(today, title[cou], links[cou], website, contents, classification,))
con.commit()