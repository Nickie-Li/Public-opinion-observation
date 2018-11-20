
# coding: utf-8

# In[41]:


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


# In[43]:


#財經
website = '聯合報'
#url = 'https://udn.com/news/breaknews/1/6#breaknews'
classification = '財經'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("-disable-setuid-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
executable_path= '/opt/google/chrome/chromedriver'
driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
driver.implicitly_wait(3)
driver.get('https://udn.com/news/breaknews/1/6#breaknews')
for i in range(1,25):
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(2)
click = driver.find_element_by_class_name("more")
click.click()
for i in range(1,5):
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(2)

title = []
dt = []
links = []

soup = BeautifulSoup(driver.page_source,'lxml')
tr = soup.select('div.area_body dl dt')
for a in tr:
    texts = a.select('h2 a')
    for t in texts:
        #print(t.text)#title
        title.append(t.text)
        l = 'https://udn.com' + t['href']
        #print(l)
        links.append(l)
    d = a.select('div.info')
    for dd in d:
        ddd = dd.select('div.dt')
        for dddd in ddd:
            #print(dddd.text)
            dt.append(dddd.text)

today = datetime.today()
today = datetime.strftime(today,'%m-%d')
#print(today)
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
    tr = soup.select('div#story_body_content p')
    contents = ''
    for t in tr:
        if(len(t.text)>1):
            contents = contents + '\n\n' + t.text.strip()
    c.execute("INSERT INTO News(dt, title, link, website, summary, content, classification) VALUES(?, ?, ?, ?, '', ?, ?)",(today, title[cou], links[cou], website, contents, classification,))
con.commit()

# In[45]:


#保險
website = '聯合報'
url = ['https://udn.com/search/result/2/%E4%BF%9D%E9%9A%AA/1', 'https://udn.com/search/result/2/%E4%BF%9D%E9%9A%AA/2', 'https://udn.com/search/result/2/%E4%BF%9D%E9%9A%AA/3']
classification = '保險'

for link in url:
    title = []
    dt = []
    links = []
    summary = []
    res = requests.get(link, headers = headers)
    soup = BeautifulSoup(res.text, 'lxml')
    tr = soup.select('div #search_content dt')
    for a in tr:
        #print(a.h2.text)
        title.append(a.h2.text)
        #print(a.a['href'])
        links.append(a.a['href'])
        #print(a.span.text)
        dt.append(a.span.text)
        #print(a.p.text)
        summary.append(a.p.text)
    today = datetime.today()
    today = datetime.strftime(today,'%m/%d')
    #print(today)
    count = 0

    for item in dt:
        if today in item:
            count = count + 1
            #print(count)
    today = datetime.today()
    today = datetime.strftime(today,'%Y/%m/%d')
    for cou in range(0,count):
        res = requests.get(links[cou], headers = headers)
        soup = BeautifulSoup(res.text, 'lxml')
        tr = soup.select('div#story_body_content p')
        contents = ''
        for t in tr:
            if(len(t.text)>1):
                contents = contents + '\n\n' + t.text.strip()
        c.execute("INSERT INTO News(dt, title, link, website, summary, content, classification) VALUES(?, ?, ?, ?, ?, ?, ?)",(today, title[cou], links[cou], website, summary[cou], contents, classification,))
con.commit()

# In[44]:


#富邦
website = '聯合報'
url = ['https://udn.com/search/result/2/%E5%AF%8C%E9%82%A6/1', 'https://udn.com/search/result/2/%E5%AF%8C%E9%82%A6/2']
classification = '富邦'

for link in url:
    title = []
    dt = []
    links = []
    summary = []
    res = requests.get(link, headers = headers)
    soup = BeautifulSoup(res.text, 'lxml')
    tr = soup.select('div #search_content dt')
    for a in tr:
        #print(a.h2.text)
        title.append(a.h2.text)
        #print(a.a['href'])
        links.append(a.a['href'])
        #print(a.span.text)
        dt.append(a.span.text)
        #print(a.p.text)
        summary.append(a.p.text)
    today = datetime.today()
    today = datetime.strftime(today,'%m/%d')
    #print(today)
    count = 0

    for item in dt:
        if today in item:
            count = count + 1
            #print(count)

    today = datetime.today()
    today = datetime.strftime(today,'%Y/%m/%d')
    for cou in range(0,count):
        res = requests.get(links[cou], headers = headers)
        soup = BeautifulSoup(res.text, 'lxml')
        tr = soup.select('div#story_body_content p')
        contents = ''
        for t in tr:
            if(len(t.text)>1):
                contents = contents + '\n\n' + t.text.strip()
        c.execute("INSERT INTO News(dt, title, link, website, summary, content, classification) VALUES(?, ?, ?, ?, ?, ?, ?)",(today, title[cou], links[cou], website, summary[cou], contents, classification,))
con.commit()
driver.quit()