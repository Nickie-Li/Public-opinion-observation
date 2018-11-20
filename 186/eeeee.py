
# coding: utf-8

# # 保險e聊站 
# http://forum.i835.com.tw/forum-f20/page00.html?sk=f

import requests 
from lxml import html
from bs4 import BeautifulSoup
from datetime import timedelta, datetime 
import time
import sqlite3 as lite
import sys
import os

# get soup

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

def pageDetail(detailUrl):
    count=0
    soup=getBeautifulHtml(detailUrl)
    
    if soup.select_one('.postbody'):
        
        title=soup.select('.postbody h3 a')[0].text

        summary=soup.select('div.postbody div.content')[0].text
        summary=summary.replace(u'\u3000',u' ').replace(u'\xa0',' ').replace("\r"," ").replace("\n"," ").replace('_','').replace('-','')
    
        #dt = soup.select('div.postbody p.author')[0].text #.split(' ',1)[1].replace(' ','').replace(',',' ')
        
        #dt = datetime.strptime(dt,'%Y-%m-%d %H:%M')
        #dt = datetime.strftime(dt,'%Y-%m-%d %H:%M:%S')
        for div in soup.select('.post'):
                count +=1
            
        count = count-1
        webnumm=1
        return{'title': title, 'summary':summary,'link':detailUrl , 'webNum':webnumm,'countMsg':count}

#第一次抓取用
#從0開始
# def dbstartWebCrawler(s,e):
#     #s=start page  e=end page
#     newsurl='http://forum.i835.com.tw/forum-f20/page{}0.html?sk=f'
#     today=getTodayStr()
    
#     tp=datetime.now()
#     tp=tp.strftime('%Y-%m-%d %H:%M:%S')
#     tp=datetime.strptime(tp,'%Y-%m-%d %H:%M:%S')
    
#     autorn=1
#     with lite.connect('../FBWEB.sqlite')as conn:
#         cur = conn.cursor()
    
#         for page in range(s,e):
#             res=requests.get(newsurl.format(page),verify=False)
#             soup=BeautifulSoup(res.text,'html.parser')
#             con=soup.select('.forumbg')[1]
            
#             for link in con.select('.row'):
#                 print(autorn)
#                 href=link.find('a', href=True)['href']    
#                 rtdb=pageDetail(href)
#                 if rtdb is None:
#                     continue
#                 else:
#                     rnumber = getTodayStr()+'2'+row_number(autorn)
#                     print(rnumber)
#                     print(href)
#                     ct=link.select('dt')[0].text.split('» ')[1].replace(',','').replace('\n','').replace('\t','')
#                     ct=chgDayType(ct)
#                     rtdb.update({'row_number':rnumber,'dt':ct})
#                     cur.execute("INSERT INTO webCrawler VALUES (:row_number, :dt, :link, :summary, :title, :webNum, :countMsg)", rtdb)
#                     autorn+=1
#         cur.execute("INSERT INTO TimeRecord VALUES (?, ?)", ('eInsurance', tp))
#         #cur.execute("UPDATE TimeRecord set last_time = ? where table_name= ?",(tp,'eInsurance'))
#dbstartWebCrawler(1,2)

#每天定時跑的
def timeWebCrawler():
    newsurl='http://forum.i835.com.tw/forum-f20/page{}0.html?sk=f'

    today=getTodayStr() #流水號用前8碼
    timePoint=getTimePoint('eInsurance')
    page=0 #網頁翻頁數
    autorn=getAutorn('webCrawler') #流水號後三碼
    wannaContinue=True
    tp=datetime.now()
    tp=tp.strftime('%Y-%m-%d %H:%M:%S')
    tp=datetime.strptime(tp,'%Y-%m-%d %H:%M:%S')
    
    with lite.connect('../FBWEB.sqlite')as conn:
        cur = conn.cursor()
        print('connect')
        while wannaContinue:
            res=requests.get(newsurl.format(page),verify=False)
            soup=BeautifulSoup(res.text,'html.parser')
            con=soup.select('.forumbg')[1]
            print(page)
            page+=1
            for link in con.select('.row'):
                ct=link.select('dt')[0].text.split('» ')[1].replace(',','').replace('\n','').replace('\t','')
                ct=chgDayType(ct)
                print(ct)
                if ct > timePoint:
                    href=link.find('a', href=True)['href']
                    rtdb=pageDetail(href)
                    if rtdb is None:
                        continue
                    else:
                        rnumber = getTodayStr()+'2'+row_number(autorn)
                        rtdb.update({'row_number':rnumber,'dt':ct})
                        cur.execute("INSERT INTO webCrawler VALUES (:row_number, :dt, :link, :summary, :title, :webNum, :countMsg)", rtdb)
                        autorn+=1
                elif ct <= timePoint:
                    wannaContinue=False
                    break
        print(tp)
        cur.execute("UPDATE TimeRecord set last_time = ? where table_name= ?",(tp,'eInsurance'))
        print('update')

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
