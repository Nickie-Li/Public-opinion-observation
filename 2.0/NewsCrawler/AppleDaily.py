
# coding: utf-8

# In[15]:


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
website = '蘋果日報'
classification = '財經'
url  = ['https://tw.finance.appledaily.com/realtime/1', 'https://tw.finance.appledaily.com/realtime/2', 'https://tw.finance.appledaily.com/realtime/3', 'https://tw.finance.appledaily.com/realtime/4']
for link in url:
    title = []
    links = []
    res = requests.get(link, headers = headers)
    soup = BeautifulSoup(res.text, 'lxml')
    tr = soup.select('li.rtddt')
    for t in tr:
        #print(t.h1.font.text)
        title.append(t.h1.font.text)
        l = 'https://tw.finance.appledaily.com' + t.a['href']
        #print(l)
        links.append(l)
    
    today = datetime.today()
    today2 = datetime.strftime(today, '%Y%m%d')
    today = datetime.strftime(today, '%m-%d')
    #print(today)
    count = 0
    for link in links:
        if today2 in link:
            count = count + 1
    
    today = datetime.today()
    today = datetime.strftime(today,'%Y/%m/%d')
    for cou in range(0,count):
        res = requests.get(links[cou], headers = headers)
        soup = BeautifulSoup(res.text, 'lxml')
        tr = soup.select('div.ndArticle_contentBox article.ndArticle_content  div.ndArticle_margin p')[:1]
        contents = ''
        for t in tr:
            if(len(t.text)>1):
                contents = contents + '\n\n' + t.text.strip()
        c.execute("INSERT INTO News(dt, title, link, website, summary, content, classification) VALUES(?, ?, ?, ?, '', ?, ?)",(today, title[cou], links[cou], website, contents, classification,))
con.commit()



#保險
website = '蘋果日報'
classification = '保險'

today = datetime.today()
y = datetime.strftime(today, '%Y')
m = datetime.strftime(today, '%m')
d = datetime.strftime(today, '%d')

today2 = datetime.strftime(today, '%Y%m%d')
today = datetime.strftime(today, '%m-%d')

url = 'https://tw.appledaily.com/search/result?sort=time&searchType=all&dateStart='+ y +'%2F'+ m +'%2F'+ d +'&dateEnd='+ y +'%2F'+ m +'%2F'+ d +'&querystrS=%E4%BF%9D%E9%9A%AA'
title = []
links = []
summary = []

res = requests.get(url,headers = headers)
soup = BeautifulSoup(res.text, 'lxml')
#print(soup)
tr = soup.select('ol#result li div.content')
for t in tr:
    #print(t.h2.a.text)
    title.append(t.h2.a.text)
    #print(t.h2.a['href'])
    links.append(t.h2.a['href'])
    #print(t.p.text)
    summary.append(t.p.text)

today = datetime.today()
today = datetime.strftime(today,'%Y/%m/%d')
for cou in range(0,len(title)):
    res = requests.get(links[cou], headers = headers)
    soup = BeautifulSoup(res.text, 'lxml')
    tr = soup.select('div.ndArticle_contentBox article.ndArticle_content  div.ndArticle_margin p')[:1]
    contents = ''
    for t in tr:
        if(len(t.text)>1):
            contents = contents + '\n\n' + t.text.strip()
    c.execute("INSERT INTO News(dt, title, link, website, summary, content, classification) VALUES(?, ?, ?, ?, ?, ?, ?)",(today, title[cou], links[cou], website, summary[cou], contents, classification,))
con.commit()



#富邦
website = '蘋果日報'
classification = '富邦'

today = datetime.today()
y = datetime.strftime(today, '%Y')
m = datetime.strftime(today, '%m')
d = datetime.strftime(today, '%d')

today2 = datetime.strftime(today, '%Y%m%d')
today = datetime.strftime(today, '%m-%d')

url = 'https://tw.appledaily.com/search/result?sort=time&searchType=all&dateStart='+ y +'%2F'+ m +'%2F'+ d +'&dateEnd='+ y +'%2F'+ m +'%2F'+ d +'&querystrS=富邦'
title = []
links = []
summary = []

res = requests.get(url,headers = headers)
soup = BeautifulSoup(res.text, 'lxml')
#print(soup)
tr = soup.select('ol#result li div.content')
for t in tr:
    #print(t.h2.a.text)
    title.append(t.h2.a.text)
    #print(t.h2.a['href'])
    links.append(t.h2.a['href'])
    #print(t.p.text)
    summary.append(t.p.text)

today = datetime.today()
today = datetime.strftime(today,'%Y/%m/%d')
for cou in range(0,len(title)):
    res = requests.get(links[cou], headers = headers)
    soup = BeautifulSoup(res.text, 'lxml')
    tr = soup.select('div.ndArticle_contentBox article.ndArticle_content  div.ndArticle_margin p')[:1]
    contents = ''
    for t in tr:
        if(len(t.text)>1):
            contents = contents + '\n\n' + t.text.strip()
    c.execute("INSERT INTO News(dt, title, link, website, summary, content, classification) VALUES(?, ?, ?, ?, ?, ?, ?)",(today, title[cou], links[cou], website, summary[cou], contents, classification,))
con.commit()