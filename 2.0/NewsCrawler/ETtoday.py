
# coding: utf-8

# In[1]:


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
website = 'Ettoday新聞雲'

classification = '財經'

today = datetime.today()
today2 = datetime.strftime(today,'%Y-%m-%d')
today = datetime.strftime(today,'%m/%d')

url = 'https://www.ettoday.net/news/news-list-' + today2 +'-17.htm'


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("-disable-setuid-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
executable_path= '/opt/google/chrome/chromedriver'
driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
driver.implicitly_wait(3)
driver.get(url)
for i in range(1,5):
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(2)

title = []
dt = []
links = []

soup = BeautifulSoup(driver.page_source,'lxml')
tr = soup.select('div.part_list_2 h3')
for h in tr:
    #print(h.a.text)
    title.append(h.a.text)
    #print(h.span.text)
    dt.append(h.span.text)
    l = 'https://www.ettoday.net/' + h.a['href']
    #print(l)
    links.append(l)

count = 0   
for item in dt:
    if today in item:
        count = count + 1
        #print(item)
            
            
today = datetime.today()
today = datetime.strftime(today,'%Y/%m/%d')
for cou in range(0,count):
    res = requests.get(links[cou], headers = headers)
    soup = BeautifulSoup(res.text, 'lxml')
    tr = soup.select('div.story p')[1:]
    contents = ''
    for t in tr:
        if(len(t.text)>1):
            contents = contents + '\n\n' + t.text.strip()
    c.execute("INSERT INTO News(dt, title, link, website, summary, content, classification) VALUES(?, ?, ?, ?, '', ?, ?)",(today, title[cou], links[cou], website, contents, classification,))
con.commit()




#保險
website = 'Ettoday新聞雲'

classification = '保險'

today = datetime.today()
today2 = datetime.strftime(today,'%Y-%m-%d')
today = datetime.strftime(today,'%m/%d')

url = 'https://www.ettoday.net/news/news-list-' + today2 +'-36.htm'


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("-disable-setuid-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
executable_path= '/opt/google/chrome/chromedriver'
driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
driver.implicitly_wait(3)
driver.get(url)
for i in range(1,5):
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(2)

title = []
dt = []
links = []

soup = BeautifulSoup(driver.page_source,'lxml')
tr = soup.select('div.part_list_2 h3')
for h in tr:
    #print(h.a.text)
    title.append(h.a.text)
    #print(h.span.text)
    dt.append(h.span.text)
    l = 'https://www.ettoday.net/' + h.a['href']
    #print(l)
    links.append(l)

count = 0   
for item in dt:
    if today in item:
        count = count + 1
        #print(item)
            
            
today = datetime.today()
today = datetime.strftime(today,'%Y/%m/%d')
for cou in range(0,count):
    res = requests.get(links[cou], headers = headers)
    soup = BeautifulSoup(res.text, 'lxml')
    tr = soup.select('div.story p')[1:]
    contents = ''
    for t in tr:
        if(len(t.text)>1):
            contents = contents + '\n\n' + t.text.strip()
    c.execute("INSERT INTO News(dt, title, link, website, summary, content, classification) VALUES(?, ?, ?, ?, '', ?, ?)",(today, title[cou], links[cou], website, contents, classification,))
con.commit()




#富邦
website = 'Ettoday新聞雲'
classification = '富邦'

url = 'https://www.ettoday.net/news_search/doSearch.php?keywords=%E5%AF%8C%E9%82%A6&kind=36&idx=2'
title = []
dt = []
links = []
summary = []
res = requests.get(url, headers = headers)
soup = BeautifulSoup(res.text,'lxml')
tr = soup.select('div.box_2')
for h in tr:
#     print(h.h2.a.text)
    title.append(h.h2.a.text)
#     print(h.span.text)
    dt.append(h.span.text)
#     print(h.h2.a['href'])
    links.append(h.h2.a['href'])
    summary.append(h.p.text.strip())

count = 0 
today = datetime.today()
today = datetime.strftime(today,'%m-%d')
#today = '06-08'

for item in dt:
    if today in item:
        count = count + 1
        
today = datetime.today()
today = datetime.strftime(today,'%Y/%m/%d')
for cou in range(0,count):
    res = requests.get(links[cou], headers = headers)
    soup = BeautifulSoup(res.text, 'lxml')
    tr = soup.select('div.story p')[1:]
    contents = ''
    for t in tr:
        if(len(t.text)>1):
            contents = contents + '\n\n' + t.text.strip()
    c.execute("INSERT INTO News(dt, title, link, website, summary, content, classification) VALUES(?, ?, ?, ?, '', ?, ?)",(today, title[cou], links[cou], website, contents, classification,))
con.commit()
driver.quit()