
# coding: utf-8

# # My83 保險網
# https://my83.com.tw/question/index?page=1


import requests 
from lxml import html
from bs4 import BeautifulSoup
from datetime import datetime 
from datetime import timedelta
import time
import sqlite3 as lite
import sys
import os


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
    


# # getPageDetail
def pageDetail(detailUrl):
    soup=getBeautifulHtml(detailUrl)
    if soup.select_one('.list-group-item'):
        title=soup.select('h1')[0].text
        title=title.replace(u'\u3000', u'  ').replace(u'\u200b','')
        title=title.split(' ',1)[1]

        summary=''.join([p.text for p in soup.select('.question-content')])
        summary=summary.replace(u'\u3000',u' ').replace(u'\xa0',' ').replace("\r"," ").replace("\n"," ").replace(' ','').replace('_','').replace('-','')
        dt = soup.select('.date')[0].text
        dt=datetime.strptime(dt,'%Y-%m-%d %H:%M')
        
        rep = soup.select('.list-group-item-text strong')[0].text
        rep = int(rep.replace('個留言',' '))
        webnumm = 1; #討論區
        return{'title': title,'dt':dt, 'summary':summary,'link':detailUrl, 'webNum':webnumm,'countMsg':rep }
    
#get messages
def pagere(detailUrl):
    soup=getBeautifulHtml(detailUrl)
    if soup.select_one('.list-group-item'):
        
        dt = soup.select('.date')[0].text
        dt=datetime.strptime(dt,'%Y-%m-%d %H:%M')
        rep = soup.select('.list-group-item-text strong')[0].text
        rep = int(rep.replace('個留言',' '))
        return{'dt':dt,'countMsg':rep}
    


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


#第一次抓取用
# def dbstartWebCrawler(s,e):
#     #s=start page  e=end page
#     newsurl='https://my83.com.tw/question/index?page={}'
#     today=getTodayStr()
    
#     tp=datetime.now()
#     tp=tp.strftime('%Y-%m-%d %H:%M:%S') 
    
#     autorn=1
#     with lite.connect('../FBWEB.sqlite')as conn:
#         cur = conn.cursor()
    
#         for page in range(s,e):
#             res=requests.get(newsurl.format(page),verify=False)
#             soup=BeautifulSoup(res.text,'html.parser')
#             for news in soup.select('.item a'):
#                 #time.sleep(1)
#                 rtdb=pageDetail('https://my83.com.tw%s'%(news['href']))
#                 if rtdb is None:
#                     continue
#                 else:
#                     rnumber = getTodayStr()+'1'+row_number(autorn)
#                     rtdb.update({'row_number':rnumber})
#                     cur.execute("INSERT INTO webCrawler VALUES (:row_number, :dt, :link, :summary, :title, :webNum, :countMsg)", rtdb)
#                     autorn+=1       
#         cur.execute("INSERT INTO TimeRecord VALUES (?, ?)", ('my83', tp))
#     conn.commit()
#     conn.close()

# dbstartWebCrawler(1,2)


#每天定時跑的
def timeWebCrawler():
    newsurl='https://my83.com.tw/question/index?page={}'
    today=getTodayStr() #流水號用前8碼
    timePoint=getTimePoint('my83')
    page=1 #網頁翻頁數
    autorn=getAutorn('webCrawler') #流水號後三碼
    wannaContinue=True
    tp=datetime.now() #存回資料庫的timepoint
    tp=tp.strftime('%Y-%m-%d %H:%M:%S') 
    ct=''
    print('aaa')
    with lite.connect('../FBWEB.sqlite')as conn:
        cur = conn.cursor()
        print('connect')
        while wannaContinue:
            res=requests.get(newsurl.format(page),verify=False)
            soup=BeautifulSoup(res.text,'html.parser')
            page+=1
            print(page)
            for news in soup.select('.item a'):
                ct=news.select('.col-sm-2 p')[0].text
                ct=chgDayType(ct)
                print(ct)
                if ct >= timePoint:
                    print('https://my83.com.tw%s'%(news['href']))
                    rtdb=pageDetail('https://my83.com.tw%s'%(news['href']))
                    if rtdb is None:
                        continue
                    else:
                        rnumber = getTodayStr()+'1'+row_number(autorn)
                        rtdb.update({'row_number':rnumber})
                        cur.execute("INSERT INTO webCrawler VALUES (:row_number, :dt, :link, :summary, :title, :webNum, :countMsg)", rtdb)
                        autorn+=1
                        print('add')
                else:
                    wannaContinue=False
                    print('bye')
                    break
            
            cur.execute("UPDATE TimeRecord set last_time = ? where table_name= ?",(tp,'my83'))



##更新回復數量
from datetime import timedelta, datetime 
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
                conn.execute("UPDATE webCrawler set countMsg = rep where dt = toto and link = row[2]")
            nnum=nnum-1


timeWebCrawler()
timeWeb()