
# coding: utf-8

# # SOGOL 論壇-產險
# http://oursogo.com/forum.php?mod=forumdisplay&fid=199&filter=author&orderby=dateline&typeid=896&page=1

#連結丟進來抓取標題、內文、時間、連結
import requests
import re
import string
from bs4 import BeautifulSoup
from datetime import datetime
import time
import pandas
import sqlite3 as lite
import sys
import os


def page(detailurl):
    res = requests.get(detailurl,verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
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
        
    if getTodayStr() == autorn[:8]:
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
    conn.close()
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


def getNextLink(detailurl):
    #url = 'http://www.eyny.com/forum-1762-9DW81WMN.html'
    res = requests.get(detailurl, verify = False)
    newsary = []
    soup = BeautifulSoup(res.text, 'html.parser')
    for news in soup.select('.pg'):
        newsary.append(news.select('.a')[0].get('href'))
        print(news.select('a')[12])
    return newsary[0]


def pageDetail(detailurl):
    soup=page(detailurl)
    # 抓取標題
    title = soup.select('.ts a')[1].text
    # 抓取摘要
    summary = soup.select('.t_f')[0].text.replace("_","").replace("u3000","").replace("-","").replace("※","").replace("*","").replace("\r"," ").replace("\n"," ").replace(" ",'').replace(u'\xa0','')
    # 抓取時間
    dt = soup.select('.authi em')[0].text.split('發表於 ')[1]
    dt = datetime.strptime(dt,'%Y-%m-%d %H:%M:%S')#時間格式轉換
    
    rep = soup.select('div.hm > span')[4].text
    webnumm = 1
    #print(rep)
        #print(dt)
        #print(title)
        #print(summary)
        #print(detailurl)
            #print(news)
            #print(soup)
    return {'title': title, 'summary': summary,'dt':dt,'link':detailurl,'webNum':webnumm,'countMsg':rep}


# def getPageLink(s,e):
# #網址輸入
#     newsurl = 'http://oursogo.com/forum.php?mod=forumdisplay&fid=199&filter=author&orderby=dateline&typeid=896&page={}'
#     today=getTodayStr()
#     tp=datetime.now()
#     tp=chgDayFormat(tp)
#     tp = tp.strftime('%Y-%m-%d %H:%M:%S')
#     tp = datetime.strptime(tp,'%Y-%m-%d %H:%M:%S')
#     autorn = 1
#     with lite.connect('../FBWEB.sqlite')as conn:
#         cur = conn.cursor()
#         for pages in range(s,e):#取連結
#             print(pages)
#             res = requests.get(newsurl.format(pages), verify = False)
#             soup = BeautifulSoup(res.text, 'html.parser')
#             #抓連結
#             for news in soup.select('.new'):
#                 link = news.select('a')[1].get('href')
#                 href = pageDetail(link)
#                 newsary = pageDetail(link)
#                 print(link)
#                 #print(newsary)
#                 if newsary is None:
#                     continue
#                 else:
#                     rnumber = getTodayStr()+'5'+row_number(autorn)#流水號
#                     #抓時間
#                     ress = requests.get(link, verify = False)                
#                     soupp = BeautifulSoup(ress.text, 'html.parser')
#                     ct = soupp.select('.authi em')[0].text.split('發表於 ')[1]
#                     ct = chgDayType(ct)
#                     newsary.update({'row_number':rnumber,'dt':ct})#更新時間
#                     print(rnumber)
#                     ##C_sogoP-----table名稱
#                     cur.execute("INSERT INTO webCrawler VALUES (:row_number, :dt, :link, :summary, :title, :webNum, :countMsg)", newsary)
#                     autorn += 1
#         cur.execute("INSERT INTO TimeRecord VALUES (?, ?)", ('sogoL', tp))##欄位----table-C_
#     conn.commit()
#     conn.close()


# getPageLink(1,3)



#每天定時跑的
def timeWebCrawler():
    newsurl='http://oursogo.com/forum.php?mod=forumdisplay&fid=199&filter=author&orderby=dateline&typeid=896&page={}'
    
    today=getTodayStr() #流水號用前8碼
    timePoint=getTimePoint('sogoL')
    
    autorn=getAutorn('webCrawler') #流水號後三碼
    #print(autorn)
    #print(timePoint)
    #print(today)
    wannaContinue=True
    page=1
    tp=datetime.now()
    tp=chgDayFormat(tp)
        
    with lite.connect('../FBWEB.sqlite')as conn:##sql
        cur = conn.cursor()
        
        while wannaContinue:
            #for pages in range(1,2):
            res=requests.get(newsurl.format(page),verify=False)
            soup=BeautifulSoup(res.text,'html.parser')
            page+=1
            if soup.select_one('.common a'):##抓連結
                    #print(soup)
                for link in soup.select('.common a'):
                    href=link['href']
                    print(href)
                    rtdb=pageDetail(href)
                    if rtdb is None:
                        continue
                    else:
                        ct=rtdb['dt']
                        if ct > timePoint:                
                            rnumber = getTodayStr()+'5'+row_number(autorn)                            
                            rtdb.update({'row_number':rnumber})
                            cur.execute("INSERT INTO webCrawler VALUES (:row_number, :dt, :link, :summary, :title, :webNum, :countMsg)", rtdb)
                            autorn+=1
                        elif ct <= timePoint:
                            continue
            else:
                 wannaContinue=False
        cur.execute("UPDATE TimeRecord set last_time = ? where table_name= ?",(tp,'sogoL'))


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
