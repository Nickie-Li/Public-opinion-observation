
# coding: utf-8

# In[8]:


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
website = '自由時報'
url = ['http://news.ltn.com.tw/list/breakingnews/business/1', 'http://news.ltn.com.tw/list/breakingnews/business/2', 'http://news.ltn.com.tw/list/breakingnews/business/3', 'http://news.ltn.com.tw/list/breakingnews/business/4', 'http://news.ltn.com.tw/list/breakingnews/business/5']
classification = '財經'
for link in url:
    title = []
    dt = []
    links = []
    res = requests.get(link, headers = headers)
    #print(res.text)
    soup = BeautifulSoup(res.text, 'lxml')
#     f = soup.find_all('table')
#    print(f)
    tr = soup.select('div.whitecon li')
    for value in tr:
        #print(value.span.text)
        dt.append(value.span.text)
        #print(value.p.text.strip())
        title.append(value.p.text.strip())
        #print(value.a['href'])
        links.append(value.a['href'])

    today = datetime.today()
    yesterday = today + timedelta(-1)
    yesterday = datetime.strftime(yesterday,'%m-%d')
    today = datetime.strftime(today,'%m/%d')
    #print(today)
    count = 0
    
    for item in dt:
        if today not in item:
            count = count + 1
            #print(count)
    
    today = datetime.today()
    today = datetime.strftime(today,'%Y/%m/%d')
    for cou in range(0,count):
        res = requests.get(links[cou], headers = headers)
        soup = BeautifulSoup(res.text, 'lxml')
        tr = soup.select('div.text p')[1:]
        contents = ''
        for t in tr:
            if(len(t.text)>1):
                contents = contents + '\n\n' + t.text.strip()
        c.execute("INSERT INTO News(dt, title, link, website, summary, content, classification) VALUES(?, ?, ?, ?, '', ?, ?)",(today, title[cou], links[cou], website, contents, classification,))
con.commit()

#保險
y = str(datetime.today().year)
m = str(datetime.today().month)
d = str(datetime.today().day)

website = '自由時報'
url = 'http://news.ltn.com.tw/search?keyword=%E4%BF%9D%E9%9A%AA&conditions=and&SYear=' + y + '&SMonth=' + m + '&SDay=' + d + '&EYear=' + y + '&EMonth=' + m + '&EDay=' + d
classification = '保險'

title = []
dt = []
links = []
summary = []
res = requests.get(url, headers = headers)
soup = BeautifulSoup(res.text, 'lxml')

tr = soup.select('ul.searchlist li')
for value in tr:
    #print(value.span.text)
    dt.append(value.span.text)
    #print(value.p.text.strip())
    title.append(value.p.text.strip())
    #print(value.a['href'])
    l=value.select('a.tit')
    for ll in l:
        link = 'http://news.ltn.com.tw/' + ll['href']
        links.append(link)
    tp = value.select('p')
    for p in tp:
        summary.append(p.text.strip())
        #print(p.text.strip())

count = 1
today = datetime.today()
today = datetime.strftime(today,'%m-%d')

for item in dt:
    if today in item:
        #print(title[count-1])
        #print(summary[count*2 - 1])
        count = count + 1
        
today = datetime.today()
today = datetime.strftime(today,'%Y/%m/%d')
for cou in range(1,count):
    res = requests.get(links[cou-1], headers = headers)
    soup = BeautifulSoup(res.text, 'lxml')
    tr = soup.select('div.text p')[1:]
    contents = ''
    for t in tr:
        if(len(t.text)>1):
            contents = contents + '\n\n' + t.text.strip()
    c.execute("INSERT INTO News(dt, title, link, website, summary, content, classification) VALUES(?, ?, ?, ?, ?, ?, ?)",(today, title[cou-1], links[cou-1], website, summary[cou*2-1], contents, classification,))
    
con.commit()

#富邦
y = str(datetime.today().year)
m = str(datetime.today().month)
d = str(datetime.today().day)

website = '自由時報'
url = 'http://news.ltn.com.tw/search?keyword=富邦&conditions=and&SYear=' + y + '&SMonth=' + m + '&SDay=' + d + '&EYear=' + y + '&EMonth=' + m + '&EDay=' + d
classification = '富邦'

title = []
dt = []
links = []
summary = []
res = requests.get(url, headers = headers)
soup = BeautifulSoup(res.text, 'lxml')

tr = soup.select('ul.searchlist li')
for value in tr:
    #print(value.span.text)
    dt.append(value.span.text)
    #print(value.p.text.strip())
    title.append(value.p.text.strip())
    #print(value.a['href'])
    l=value.select('a.tit')
    for ll in l:
        link = 'http://news.ltn.com.tw/' + ll['href']
        links.append(link)
        #print(link)
    tp = value.select('p')
    for p in tp:
        summary.append(p.text.strip())
        #print(p.text.strip())

count = 0
today = datetime.today()
today = datetime.strftime(today,'%m-%d')

for item in dt:
    if today in item:
        count = count + 1
        #print(count)

today = datetime.today()
today = datetime.strftime(today,'%Y/%m/%d')
for cou in range(1,count):
    res = requests.get(links[cou-1], headers = headers)
    soup = BeautifulSoup(res.text, 'lxml')
    tr = soup.select('div.text p')[1:]
    contents = ''
    for t in tr:
        if(len(t.text)>1):
            contents = contents + '\n\n' + t.text.strip()
    c.execute("INSERT INTO News(dt, title, link, website, summary, content, classification) VALUES(?, ?, ?, ?, ?, ?, ?)",(today, title[cou-1], links[cou-1], website, summary[cou*2-1], contents, classification,))
    
con.commit()