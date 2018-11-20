
# coding: utf-8

# # ptt

#連結丟進來抓取標題、內文、時間、連結
import requests
import re
import string
from bs4 import BeautifulSoup
from datetime import timedelta, datetime 
import time
import sqlite3 as lite
import sys
import os

requests.packages.urllib3.disable_warnings()##消紅框

def pages(detailurl):
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


class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False



def pageDetail(detailurl):
    soup = pages(detailurl)
    count=0
    try:
        summary = ' '.join([p.text for p in soup.select('#main-container')]).split('--')[0].split('2018')[1].replace("_","").replace("-","").replace("\u3000","").replace("...","").replace("※","").replace("~~~","").replace(u'\3000','').replace("**","").replace("\r"," ").replace("\n"," ").replace(" ",'').replace("==",'').replace(u'\xa0','').replace(u'\3000','')
        dt = soup.select('.article-meta-value')[3].text#抓取時間article-meta-value
        dt = datetime.strptime(dt,'%a %b %d %H:%M:%S %Y')#時間格式轉換
        
        for div in soup.select('.push'):
                count +=1
        webnumm=1 #討論區
        # 抓取標題
        for title in soup.select('.article-meta-value')[2]:
            pattern = re.compile(r'Re*')
            pattern1 = re.compile(r'Fw*')
            pattern2 = re.compile(r'\［*')
            pattern3 = re.compile(r'\[*')
            match = pattern.match(title)
            match1 = pattern1.match(title)
            match2 = pattern2.match(title)
            match3 = pattern3.match(title) 
            if match:
                title = title.split("Re:")[1]
                if match2:
                    title = title.split("]")[1]
                    break
                elif match3:
                    title = title.split("〕")[1]
                    break
            elif match1:
                title =title.split("Fw:")[1]
                if match2:
                    title = title.split("]")[1] 
                    break
                elif match3:
                    title = title.split("〕")[1]
                    break
            else:
                if match2:
                    title 
                    break
                elif match3:
                    title = title.split("〕")[1]
                    break
                else:
                    title
        return {'title': title, 'summary': summary,'dt':dt,'link':detailurl, 'webNum':webnumm,'countMsg':count}
    except:
        return None


#get next page's link
#def getNextLink(url):
#    soup=pages(url)
#    nextpg=soup.select('.wide')[1].get('href')
#    return 'https://www.ptt.cc'+nextpg
#    

#每天定時跑的
def timeWebCrawler():
    newsurl='https://www.ptt.cc/bbs/Insurance/index{}.html'
    today=getTodayStr() #流水號用前8碼
    timePoint=getTimePoint('ptt')
    autorn=getAutorn("webCrawler") #流水號後三碼
    wannaContinue=True
    tp=datetime.now()
    tp=chgDayFormat(tp)

    with lite.connect('../FBWEB.sqlite')as conn:##sql
        cur = conn.cursor()
        print('connect')
        new = 'https://www.ptt.cc/bbs/Insurance/index.html'
        
        res = requests.get(new, verify = False)
        soup = BeautifulSoup(res.text, 'html.parser')
        pa = soup.select('.action-bar a')[3].get('href')
        pa = int(pa[-9:].replace('.html',''))
        pa = pa + 1
        pa1 = pa -5
        new1 = 'https://www.ptt.cc/bbs/Insurance/index{}.html'
        #換頁抓取
        for pages in range(pa,pa1,-1):
            print(pages)
            res = requests.get(newsurl.format(pages), verify = False)
            print(newsurl.format(pages))
            soup = BeautifulSoup(res.text, 'html.parser')
            #res = requests.get(newsurl, verify = False)
            #soup = BeautifulSoup(res.text, 'html.parser')
            #newsurl=getNextLink(newsurl)
            for news in soup.select('.r-ent'):
                title = news.select('.title')[0].text.replace('	','').replace(' ','').replace('\r','').replace('\n','')
                print(title)
                if re.match(r'\(本文已被刪除\)*',title):
                    continue
                elif re.match(r'\[公告\]*',title):
                    continue
                elif re.match(r'\<\w+\>未刪除說明文字',title):
                    continue
                elif re.match(r'\<\w+\>請按險種格式重發文',title):
                    continue
                elif re.match(r'\<\w+\>板規三',title):
                    continue
                elif re.match(r'\<\w+\>請按險種格式重新發文',title):
                    continue
                elif re.match(r'\<\w+\>資料過於簡略',title):
                    continue
                elif re.search( r'<*>', title, re.M|re.I):
                    continue
                elif news.select('.mark')[0].text:
                    continue
                else:
                    for new in news.select('.title'):
                        link = new.select('a')[0].get('href')                            
                        print("https://www.ptt.cc%s"%(link))
                        newsary = pageDetail("https://www.ptt.cc%s"%(link))                            
                        if newsary is None:
                            continue
                        else:
                            ct=newsary['dt']##判斷時間
                           
                            #print(ct)
                            #print(timePoint)
                            #a = timePoint + timedelta(-2)
                            if ct > timePoint:
                                ress = requests.get("https://www.ptt.cc%s"%(link), verify = False)                
                                soupp = BeautifulSoup(ress.text, 'html.parser')
                                ct = soupp.select('.article-meta-value')[3].text
                                ct = datetime.strptime(ct,'%a %b %d %H:%M:%S %Y')
                                ct = chgDayType(str(ct))
                                rnumber = getTodayStr()+'7'+row_number(autorn)
                                newsary.update({'row_number':rnumber,'dt':ct})#更新時間
                                cur.execute("INSERT INTO webCrawler VALUES (:row_number, :dt, :link, :summary, :title, :webNum, :countMsg)", newsary)
                                autorn+=1
                                print('add')
                            else:
                                print('bye')
                                break
                                
                    cur.execute("UPDATE TimeRecord set last_time = ? where table_name= ?",(tp,'ptt'))

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
