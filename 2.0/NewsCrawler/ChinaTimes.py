
# coding: utf-8

# In[9]:


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
website = '中時電子報'
url = ['http://www.chinatimes.com/realtimenews/16-260410?page=1', 'http://www.chinatimes.com/realtimenews/16-260410?page=2']
classification = '財經'

for link in url:
    title = []
    dt = []
    links = []
    res = requests.get(link, headers = headers)
    soup = BeautifulSoup(res.text, 'lxml')
    tr = soup.select('div.listRight li.clear-fix')
    for a in tr:
        #print(a.h2.a.text.strip())
        title.append(a.h2.a.text.strip())
        l = 'http://www.chinatimes.com/' + a.h2.a['href']
        #print(l)
        links.append(l)
        #print(a.time.text)
        dt.append(a.time.text)

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
        tr = soup.select('article.arttext p')
        contents = ''
        for t in tr:
            if(len(t.text)>1):
                contents = contents + '\n\n' + t.text.strip()
        c.execute("INSERT INTO News(dt, title, link, website, summary, content, classification) VALUES(?, ?, ?, ?, '', ?, ?)",(today, title[cou], links[cou], website, contents, classification,))
con.commit()



#保險
classification = '保險'
website = '中時電子報'
url = 'http://www.chinatimes.com/search/result.htm?q=%E4%BF%9D%E9%9A%AA#gsc.tab=0&gsc.q=%E4%BF%9D%E9%9A%AA&gsc.sort=date'
#url = 'http://www.chinatimes.com/'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("-disable-setuid-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
executable_path= '/opt/google/chrome/chromedriver'
driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
driver.implicitly_wait(3)
driver.get(url)

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
# nextpage = driver.find_elements_by_class_name("gsc-cursor-page")[1]
# nextpage.click()
# driver.refresh()
url = 'http://www.chinatimes.com/search/result.htm?q=%E4%BF%9D%E9%9A%AA#gsc.tab=0&gsc.q=%E4%BF%9D%E9%9A%AA&gsc.sort=date&gsc.page=2'
driver.get(url)
url2 = driver.find_elements_by_tag_name("a")
url2 = driver.find_elements_by_class_name("gs-title")
su2 = driver.find_elements_by_class_name("gs-snippet")
links = linksearch(links, url2)
title = titlesearch(title, url2)
summary = summarysearch(summary, su2)
#result2 = search(result1, link2)
driver.refresh()
url = 'http://www.chinatimes.com/search/result.htm?q=%E4%BF%9D%E9%9A%AA#gsc.tab=0&gsc.q=%E4%BF%9D%E9%9A%AA&gsc.sort=date&gsc.page=3'
driver.get(url)


url3 = driver.find_elements_by_tag_name("a")
url3 = driver.find_elements_by_class_name("gs-title")
su3 = driver.find_elements_by_class_name("gs-snippet")
links = linksearch(links, url3)
title = titlesearch(title, url3)
summary = summarysearch(summary, su3)
url = 'http://www.chinatimes.com/search/result.htm?q=%E4%BF%9D%E9%9A%AA#gsc.tab=0&gsc.q=%E4%BF%9D%E9%9A%AA&gsc.sort=date&gsc.page=4'
driver.get(url)


url4 = driver.find_elements_by_tag_name("a")
url4 = driver.find_elements_by_class_name("gs-title")
su4 = driver.find_elements_by_class_name("gs-snippet")
links = linksearch(links, url4)
title = titlesearch(title, url4)
summary = summarysearch(summary, su4)
#result4 = search(result3, link4)
driver.refresh()
url = 'http://www.chinatimes.com/search/result.htm?q=%E4%BF%9D%E9%9A%AA#gsc.tab=0&gsc.q=%E4%BF%9D%E9%9A%AA&gsc.sort=date&gsc.page=5'
driver.get(url)

url5 = driver.find_elements_by_tag_name("a")
url5 = driver.find_elements_by_class_name("gs-title")
su5 = driver.find_elements_by_class_name("gs-snippet")
links = linksearch(links, url5)
summary = summarysearch(summary, su5)
#result5 = search(result4, link5)
#print(len(title5)/2)
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
    tr = soup.select('article.clear-fix p')
    contents = ''
    for t in tr:
        if(len(t.text)>1):
            contents = contents + '\n\n' + t.text.strip()
    c.execute("INSERT INTO News(dt, title, link, website, summary, content, classification) VALUES(?, ?, ?, ?, ?, ?, ?)",(today, title[2*cou], links[2*cou], website, summary[cou], contents, classification,))
con.commit()



#富邦
classification = '富邦'
website = '中時電子報'
urlist = []
for i in range(1,5):
    i = str(i)
    urlist.append('http://www.chinatimes.com/search/result.htm?q=%E5%AF%8C%E9%82%A6#gsc.tab=0&gsc.q=%E5%AF%8C%E9%82%A6&gsc.sort=date&gsc.page=' + i)
for url in urlist:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("-disable-setuid-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    executable_path= '/opt/google/chrome/chromedriver'
    driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
    driver.implicitly_wait(3)

    driver.get(url)
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

    url2 = driver.find_elements_by_tag_name("a")
    url2 = driver.find_elements_by_class_name("gs-title")
    su2 = driver.find_elements_by_class_name("gs-snippet")
    links = linksearch(links, url2)
    title = titlesearch(title, url2)
    summary = summarysearch(summary, su2)
    #result2 = search(result1, link2)
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
        tr = soup.select('article.clear-fix p')
        contents = ''
        for t in tr:
            if(len(t.text)>1):
                contents = contents + '\n\n' + t.text.strip()
        c.execute("INSERT INTO News(dt, title, link, website, summary, content, classification) VALUES(?, ?, ?, ?, ?, ?, ?)",(today, title[2*cou], links[2*cou], website, summary[cou], contents, classification,))
con.commit()
driver.quit()