# coding: utf-8

# # 保險雲世代 Insurance_cloud_generation
# http://www.tw-insurance.info/forum/topic-b1.cfm?f=100


import requests 
from lxml import html
from bs4 import BeautifulSoup
from datetime import datetime 
from datetime import timedelta
import time
import pandas
import sqlite3 as lite
import sys
import os


# In[2]:


requests.packages.urllib3.disable_warnings()


# # getBeautifulHtml(url)
def getBeautifulHtml(url):
    #設定header讓他能夠不被發現是爬蟲程式
    headers ={
        """User-Agent""":"""Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"""
    }
    res=requests.get(url,headers = headers,verify=False)
    soup=BeautifulSoup(res.text,'html.parser')
    
    return soup


#流水號用日期
def getTodayStr(): 
    today=datetime.today()
    today=datetime.strftime(today,'%Y%m%d')
    return today

#流水號後三碼 補位 補三位 
def row_number(number):
    n="%05d" %number
    return n 

#判斷流水號是否從1開始排序
def getAutorn(webCrawler):
    with lite.connect('../FBWEB.sqlite')as conn:
        cur = conn.cursor()
        cur.execute("SELECT max(rowNumber) FROM '%s'" %(webCrawler));
    for row in cur:
        autorn=row[0]
        
    if getTodayStr() ==autorn[:8]:
        return int(autorn[9:])+1
    else:
        return 1

def getTimePoint(table_name):
    timePoint=''
    with lite.connect('../FBWEB.sqlite')as conn:
        cur = conn.cursor()
        cur.execute("SELECT last_time FROM TimeRecord WHERE table_name ='%s'" %(table_name));
    for row in cur:
        timePoint=row[0]
    timePoint=chgDayType(timePoint)
    return timePoint   
        
        
def chgDayType(oneTime):
    oneTime=oneTime.replace('/','-')
    try:
        oneTime=datetime.strptime(oneTime,"%Y-%m-%d %H:%M")
        oneTime=chgDayFormat(oneTime)
        return oneTime
    except:
        oneTime=datetime.strptime(oneTime,"%Y-%m-%d %H:%M:%S")
        return oneTime
    
def chgDayFormat(oneTime):
    #讓格式都是 "%Y-%m-%d %H:%M:%S"
    oneTime=datetime.strftime(oneTime,"%Y-%m-%d %H:%M:%S")
    oneTime=datetime.strptime(oneTime,"%Y-%m-%d %H:%M:%S")
    return oneTime


# # pageDetail(detailurl)

# In[6]:


def pageDetail(detailurl):
    soup=getBeautifulHtml(detailurl)
    count=0
    if soup.select('h2'):
        # 抓取標題
        title = soup.select('h2')[0].text
        if title =="(管理員刪除)":
            return None
        else:
            # 抓取摘要
            summary = soup.select('.topic_content')[0].text.replace(u'\xa0',' ').replace("_"," ").replace("\r"," ").replace("\n"," ").replace(" ",'').replace('_','').replace('-','')

            # 抓取時間
            dt = soup.select('.topic_date')[0].text
            dt=chgDayType(dt) #時間格式轉換
            
            for div in soup.select('.topic_date'):
                count +=1
            count = count-1
            webnumm = 1; #討論區
            return {'title': title, 'summary': summary, 'dt':dt, 'link':detailurl , 'webNum':webnumm,'countMsg':count}
    else:
        return None


def getPageLink(s,e):
#網址輸入
    newsurl = 'http://www.tw-insurance.info/forum/topic-b1.cfm?f=100&p={}'
    newsary = []
    for pages in range(s,e):

        res = requests.get(newsurl.format(pages), verify = False)
        soup = BeautifulSoup(res.text, 'html.parser')

        for news in soup.select('.topic a'):
            newsary.append(pageDetail("http://www.tw-insurance.info/forum/%s"%(news['href'])))
    return newsary




#第一次抓取用
#從0開始

# def dbstartWebCrawler(s,e):
#     #s=start page  e=end page
#     newsurl = 'http://www.tw-insurance.info/forum/topic-b1.cfm?f=100&p={}'
#     today=getTodayStr()

#     tp=datetime.now()
#     tp=chgDayFormat(tp)
    
#     autorn=1
#     with lite.connect('../FBWEB.sqlite')as conn:
#         cur = conn.cursor()
    
#         for page in range(s,e):
#             res=requests.get(newsurl.format(page),verify=False)
#             soup=BeautifulSoup(res.text,'html.parser')
            
#             for news in soup.select('.topic a'):

#                 href=(news['href'])
#                 print('check'+""+href)
#                 rtdb=pageDetail(href)
                
#                 if rtdb is None:
#                     continue
#                 else:
#                     rnumber = getTodayStr()+'6'+row_number(autorn)
#                     print(rnumber)
#                     print(href)
                    
#                     rtdb.update({'row_number':rnumber})
#                     cur.execute("INSERT INTO webCrawler VALUES (:row_number, :dt, :link, :summary, :title, :webNum, :countMsg)", rtdb)
#                     autorn+=1
                    
#         cur.execute("INSERT INTO TimeRecord VALUES (?, ?)", ('icg', tp))
#         #cur.execute("UPDATE TimeRecord set last_time = ? where table_name= ?",(tp,'eInsurance'))

#dbstartWebCrawler(1,4)



#每天定時跑的
def timeWebCrawler():
    newsurl = 'http://www.tw-insurance.info/forum/topic-b1.cfm?f=100&p={}'

    today=getTodayStr() #流水號用前8碼
    timePoint=getTimePoint('icg')
    autorn=getAutorn('webCrawler') #流水號後三碼
    wannaContinue=True
    page=1
    tp=datetime.now()
    tp=chgDayFormat(tp)
    
    with lite.connect('../FBWEB.sqlite')as conn:
        cur = conn.cursor()
    
        while wannaContinue:
            res=requests.get(newsurl.format(page),verify=False)
            soup=BeautifulSoup(res.text,'html.parser')
            page+=1
            if soup.select('.topic a'):
                for link in soup.select('.topic a'):
                    href=link['href']
                    rtdb=pageDetail(href)
                    if rtdb is None:
                        continue
                    else:
                        ct=rtdb['dt']
                        if ct > timePoint:
                            rnumber = getTodayStr()+'6'+row_number(autorn)
                            rtdb.update({'row_number':rnumber})
                            cur.execute("INSERT INTO webCrawler VALUES (:row_number, :dt, :link, :summary, :title, :webNum, :countMsg)", rtdb)
                            autorn+=1
                        elif ct <= timePoint:
                            continue

            else:
                wannaContinue=False
        cur.execute("UPDATE TimeRecord set last_time = ? where table_name= ?",(tp,'icg'))


##更新回復數量
def timeWeb():
    today=getTodayStr() #流水號用前8碼
    tp=datetime.now()
    tp=chgDayFormat(tp)
    ##加入回覆
    nnum = 7 ##七天前資料
    while nnum==0:
        toto = tp + timedelta(-1)
        with lite.connect('../FBWEB.sqlite')as con:
            conn = con.cursor()
            conn.execute("SELECT link FROM webCrawler WHERE dt = toto")
            for row in conn:
                pageDetail(row[2])
                conn.execute("UPDATE webCrawler set countMsg = count where dt = toto and link = row[2]")
            nnum=nnum-1

timeWebCrawler()
timeWeb()
