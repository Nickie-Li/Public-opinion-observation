
# coding: utf-8

# In[24]:


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



def titlesearch(tiresult, urllist):
    for link in urllist:
        title = link.text
        if(len(title) > 0):
            #print(title)
            tiresult.append(title)
    return tiresult

def linksearch(liresult, urllist):
    for link in urllist:
        href = link.get_attribute("href")
        if(href != None):
            #print(href)
            liresult.append(href)
    return liresult

def summarysearch(suresult, urllist):
    for link in urllist:
        summ = link.text
        if(summ != None):
            #print(href)
            suresult.append(summ)
    return suresult



#財經
website = '今日新聞'
classification = '財經'
url = 'https://www.nownews.com/cat/finance?from=nav'
title = []
dt = []
links = []


res = requests.get(url, headers = headers)
soup = BeautifulSoup(res.text, 'lxml')
tr = soup.select('a.box_1y1g2yy')

for value in tr:
    #print(value.h3.text)
    title.append(value.h3.text)
    l = 'https://www.nownews.com' + value['href']
    #print(l)
    links.append(l)
    #print(value.span.text)
    dt.append(value.span.text)

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
    tr = soup.select('article.box_6sqckh.fontSize16 p')
    contents = ''
    for t in tr:
        if(len(t.text)>1):
            contents = contents + '\n\n' + t.text.strip()
    c.execute("INSERT INTO News(dt, title, link, website, summary, content, classification) VALUES(?, ?, ?, ?, '', ?, ?)",(today, title[cou], links[cou], website, contents, classification,))
con.commit()



#保險
website = '今日新聞'
classification = '保險'
url = 'https://www.nownews.com/search?keyword=%E4%BF%9D%E9%9A%AA#gsc.tab=0&gsc.q=%E4%BF%9D%E9%9A%AA&gsc.sort=date'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("-disable-setuid-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
executable_path= '/opt/google/chrome/chromedriver'
driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
driver.implicitly_wait(3)
driver.get(url)
driver.refresh()

url1 = driver.find_elements_by_tag_name("a")
url1 = driver.find_elements_by_class_name("gs-title")
su1 = driver.find_elements_by_class_name("gs-snippet")
#print(links)
links = []
title = []
summary = []
links = linksearch(links, url1)
title = titlesearch(title, url1)
summary = summarysearch(summary, su1)
driver.refresh()

counter = 0
for item in summary:
    if '天前' not in item and len(item) > 0:
        counter = counter + 1
        #print(item)
    else:
        break

driver.close()

today = datetime.today()
today = datetime.strftime(today,'%Y/%m/%d')
for cou in range(0,counter):
    res = requests.get(links[2*cou], headers = headers)
    soup = BeautifulSoup(res.text, 'lxml')
    tr = soup.select('article.box_6sqckh.fontSize16 p')
    contents = ''
    for t in tr:
        if(len(t.text)>1):
            contents = contents + '\n\n' + t.text.strip()
    c.execute("INSERT INTO News(dt, title, link, website, summary, content, classification) VALUES(?, ?, ?, ?, ?, ?, ?)",(today, title[2*cou], links[2*cou], website, summary[cou], contents, classification,))
con.commit()


#富邦
website = '今日新聞'
classification = '富邦'
url = 'https://www.nownews.com/search?keyword=%E5%AF%8C%E9%82%A6#gsc.tab=0&gsc.q=%E5%AF%8C%E9%82%A6&gsc.sort=date'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("-disable-setuid-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
executable_path= '/opt/google/chrome/chromedriver'
driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
driver.implicitly_wait(3)
driver.get(url)
driver.refresh()

url1 = driver.find_elements_by_tag_name("a")
url1 = driver.find_elements_by_class_name("gs-title")
su1 = driver.find_elements_by_class_name("gs-snippet")
#print(links)
links = []
title = []
summary = []
links = linksearch(links, url1)
title = titlesearch(title, url1)
summary = summarysearch(summary, su1)
driver.refresh()
counter = 0
for item in summary:
    if '天前' not in item and len(item) > 0:
        counter = counter + 1
    else:
        break

driver.close()

today = datetime.today()
today = datetime.strftime(today,'%Y/%m/%d')
for cou in range(0,counter):
    res = requests.get(links[2*cou], headers = headers)
    soup = BeautifulSoup(res.text, 'lxml')
    tr = soup.select('article.box_6sqckh.fontSize16 p')
    contents = ''
    for t in tr:
        if(len(t.text)>1):
            contents = contents + '\n\n' + t.text.strip()
    c.execute("INSERT INTO News(dt, title, link, website, summary, content, classification) VALUES(?, ?, ?, ?, ?, ?, ?)",(today, title[2*cou], links[2*cou], website, summary[cou], contents, classification,))
con.commit()
driver.quit()