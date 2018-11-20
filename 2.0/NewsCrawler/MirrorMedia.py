
# coding: utf-8

# In[33]:


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


def crawlerinside(lists):
    today = datetime.today()
    today = datetime.strftime(today, '%Y.%m.%d')
    count = 0

    for link in links:
        res = requests.get(link, headers = headers)
        soup = BeautifulSoup(res.text, 'lxml')
        tr = soup.select('div.article__basic-info div.article__date')
        for t in tr:
            if today in t.text:
                count = count + 1
            else:
                return count


website = '鏡週刊'
classification = '財經'
url = 'https://www.mirrormedia.mg/section/businessmoney'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("-disable-setuid-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
executable_path= '/opt/google/chrome/chromedriver'
driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
driver.implicitly_wait(3)
driver.get(url)
for i in range(1,3):
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(1)

title = []
links = []
summary = []

soup = BeautifulSoup(driver.page_source,'lxml')
tr = soup.select('div.listArticleBlock div.listArticleBlock__content a.')
count = 0
for value in tr:
    if(count % 2 != 1):
        title.append(value.text)
        l = 'https://www.mirrormedia.mg' + value['href']
        links.append(l)
        #print(value.text)
        #print(l)
    else:
        summary.append(value.text)
        #print(value.text)
    count = count + 1
#print(links)
k = crawlerinside(links)
#print(k)


today = datetime.today()
today = datetime.strftime(today,'%Y/%m/%d')
            
for cou in range(0,k):
    res = requests.get(links[cou], headers = headers)
    soup = BeautifulSoup(res.text, 'lxml')
    tr = soup.select('div.content p')
    contents = ''
    for t in tr:
        if(len(t.text)>1):
            contents = contents + '\n\n' + t.text.strip()
    c.execute("INSERT INTO News(dt, title, link, website, summary, content, classification) VALUES(?, ?, ?, ?, '', ?, ?)",(today, title[cou], links[cou], website, contents, classification,))
con.commit()


website = '鏡週刊'
classification = '保險'
url = 'https://www.mirrormedia.mg/search/%E4%BF%9D%E9%9A%AA'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("-disable-setuid-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
executable_path= '/opt/google/chrome/chromedriver'
driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
driver.implicitly_wait(3)
driver.get(url)
for i in range(1,3):
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(1)

title = []
links = []
summary = []

soup = BeautifulSoup(driver.page_source,'lxml')
tr = soup.select('div.listArticleBlock div.listArticleBlock__content a.')
count = 0
for value in tr:
    if(count % 2 != 1):
        title.append(value.text)
        l = 'https://www.mirrormedia.mg' + value['href']
        links.append(l)
        #print(value.text)
        #print(l)
    else:
        summary.append(value.text)
        #print(value.text)
    count = count + 1
        
k = crawlerinside(links)
#print(k)

today = datetime.today()
today = datetime.strftime(today,'%Y/%m/%d')
            
for cou in range(0,k):
    res = requests.get(links[cou], headers = headers)
    soup = BeautifulSoup(res.text, 'lxml')
    tr = soup.select('div.content p')
    contents = ''
    for t in tr:
        if(len(t.text)>1):
            contents = contents + '\n\n' + t.text.strip()
    c.execute("INSERT INTO News(dt, title, link, website, summary, content, classification) VALUES(?, ?, ?, ?, '', ?, ?)",(today, title[cou], links[cou], website, contents, classification,))
con.commit()



website = '鏡週刊'
classification = '富邦'
url = 'https://www.mirrormedia.mg/search/%E5%AF%8C%E9%82%A6'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("-disable-setuid-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
executable_path= '/opt/google/chrome/chromedriver'
driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
driver.implicitly_wait(3)
driver.get(url)
for i in range(1,3):
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(1)

title = []
links = []
summary = []

soup = BeautifulSoup(driver.page_source,'lxml')
tr = soup.select('div.listArticleBlock div.listArticleBlock__content a.')
count = 0
for value in tr:
    if(count % 2 != 1):
        title.append(value.text)
        l = 'https://www.mirrormedia.mg' + value['href']
        links.append(l)
        #print(value.text)
        #print(l)
    else:
        summary.append(value.text)
        #print(value.text)
    count = count + 1
        
k = crawlerinside(links)
#print(k)
            
today = datetime.today()
today = datetime.strftime(today,'%Y/%m/%d')
for cou in range(0,k):
    res = requests.get(links[cou], headers = headers)
    soup = BeautifulSoup(res.text, 'lxml')
    tr = soup.select('div.content p')
    contents = ''
    for t in tr:
        if(len(t.text)>1):
            contents = contents + '\n\n' + t.text.strip()
    c.execute("INSERT INTO News(dt, title, link, website, summary, content, classification) VALUES(?, ?, ?, ?, '', ?, ?)",(today, title[cou], links[cou], website, contents, classification,))
con.commit()
driver.quit()