
# coding: utf-8

# In[1]:


import smtplib
import datetime
import sqlite3
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.text import MIMEText
import sys
from os import path
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from datetime import datetime,timedelta ,date,time
currentday = datetime.today()
connect = sqlite3.connect('../FBWEB.sqlite')
c = connect.cursor()
c.row_factory = lambda cursor, row: row[0]
con = connect.cursor()
sender = 'it.crawler@fubon.com'


# In[2]:


currentday = datetime.today()
startday = currentday + timedelta(-1)
str_startday = datetime.strftime(startday,'%Y/%m/%d')
str_startday2 = datetime.strftime(startday,'%Y-%m-%d')
stamp_startday = datetime.strptime(str_startday2,'%Y-%m-%d')

lastweek_start = currentday + timedelta(-(currentday.weekday()+7))
str_lastweek_start = datetime.strftime(lastweek_start,'%Y/%m/%d')
str_lastweek_start2 = datetime.strftime(lastweek_start,'%Y-%m-%d')
stamp_lastweek_start = datetime.strptime(str_lastweek_start2,'%Y-%m-%d')

lastweek_end = currentday.date() + timedelta(-(currentday.weekday()))
str_lastweek_end = datetime.strftime(lastweek_end,'%Y/%m/%d')
str_lastweek_end2 = datetime.strftime(lastweek_end,'%Y-%m-%d')
stamp_lastweek_end = datetime.strptime(str_lastweek_end2,'%Y-%m-%d')

lastmonth_end = currentday.date() + timedelta(-(currentday.day))
lastmonth_start = currentday + timedelta(-(lastmonth_end.day+currentday.day-1))
str_lastmonth_end = datetime.strftime(lastmonth_end,'%Y/%m/%d')
str_lastmonth_start = datetime.strftime(lastmonth_start,'%Y/%m/%d')
str_lastmonth_end2 = datetime.strftime(lastmonth_end,'%Y-%m-%d')
str_lastmonth_start2 = datetime.strftime(lastmonth_start,'%Y-%m-%d')
stamp_lastmonth_end = datetime.strptime(str_lastmonth_end2,'%Y-%m-%d')
stamp_lastmonth_start = datetime.strptime(str_lastmonth_start2,'%Y-%m-%d')

currentday2 = datetime.strftime(currentday,'%Y-%m-%d')
currentday1 = datetime.strptime(currentday2,'%Y-%m-%d')
currentday = datetime.strftime(currentday,'%Y/%m/%d')


# In[3]:


#日
def content1(addr, keyword):
    keywords = [x.strip() for x in keyword.split(',')]
    lis = []
    lilink = []
    lititle = c.execute("""SELECT title FROM News WHERE dt = ?""",(str_startday,)).fetchall()
    for k in keywords:
        for l in lititle:
            if k in l:
                if l not in lis:
                    lis.append(l)
                    link = c.execute("""SELECT link FROM News WHERE title = ? """,(l,)).fetchone()
                    lilink.append(link)
            else:
                t = c.execute("""SELECT summary FROM News WHERE title = ? """,(l,)).fetchone()
                if k in t:
                    if l not in lis:
                        lis.append(l)
                        link = c.execute("""SELECT link FROM News WHERE title = ? """,(l,)).fetchone()
                        lilink.append(link)
    
    di = list()
    for e in range(0, len(lis)):
        k = '</li>' + lis[e] + ' : <br />' + lilink[e]
        di.append(k)
    inserted_list = '</li>'.join([x.strip() for x in di])
    
    dayi = list()
    daytitle = c.execute("""SELECT title FROM WebCrawler  WHERE dt >= ? AND dt < ? ORDER BY countMsg DESC LIMIT 10""",(stamp_startday,currentday1,)).fetchall()
    daylink = c.execute("""SELECT link FROM WebCrawler  WHERE dt >= ? AND dt < ? ORDER BY countMsg DESC LIMIT 10""",(stamp_startday,currentday1,)).fetchall()
    daylist = list()
    for e in range(0, len(daytitle)):
        k = '</li>' + daytitle[e] + ' : <br/>' + daylink[e]
        dayi.append(k)
    day_list = '</li>'.join([x.strip() for x in dayi])
    
    
    period = str_startday
    msgText = MIMEText("""    <h4>Hi,</h4>
    <p>We have updated the website!</p>
    <p>參考日期:"""+ period + """</p>
    <div><img src="cid:image1" height="600" width="600"></div>
    <p>文章列表</p>
    <ul>%s"""% (day_list,) + """</ul>
    <br/>
    <p>""" + keyword + """  相關文章:</p>
    <div>
    <ul>%s</ul>
    <br />
    <h3>Best Regard</h3></div>""" % (inserted_list,),'html','utf-8') 
    
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = 'Fubon Word Cloud' 
    msgRoot.attach(msgText)
    fp = open('static/img/daily.jpg','rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage)
    
    smtp.sendmail(sender, addr, msgRoot.as_string())


# In[4]:


#週
def content2(addr, keyword):
    keywords = [x.strip() for x in keyword.split(',')]
    lis = []
    lilink = []
    lititle = c.execute("""SELECT title FROM News WHERE dt >= ? AND dt <= ? """,(str_lastweek_start,str_lastweek_end,)).fetchall()
    for k in keywords:
        for l in lititle:
            if k in l:
                if l not in lis:
                    lis.append(l)
                    link = c.execute("""SELECT link FROM News WHERE title = ? """,(l,)).fetchone()
                    lilink.append(link)
            else:
                t = c.execute("""SELECT summary FROM News WHERE title = ? """,(l,)).fetchone()
                if k in t:
                    if l not in lis:
                        lis.append(l)
                        link = c.execute("""SELECT link FROM News WHERE title = ? """,(l,)).fetchone()
                        lilink.append(link)

    di = list()
    for e in range(0, len(lis)):
        k = '</li>' + lis[e] + ' : <br />' + lilink[e]
        di.append(k)
    inserted_list = '</li>'.join([x.strip() for x in di])
    
    weeki = list()
    weektitle = c.execute("""SELECT title FROM WebCrawler  WHERE dt > ? AND dt < ? ORDER BY countMsg DESC LIMIT 10""",(stamp_lastweek_start,stamp_lastweek_end)).fetchall()
    weeklink = c.execute("""SELECT link FROM WebCrawler  WHERE dt > ? AND dt < ? ORDER BY countMsg DESC LIMIT 10""",(stamp_lastweek_start,stamp_lastweek_end)).fetchall()
    weeklist = list()
    for e in range(0, len(weektitle)):
        k = '</li>' + weektitle[e] + ' : <br/>' + weeklink[e]
        weeki.append(k)
    week_list = '</li>'.join([x.strip() for x in weeki])
    
    period = str_lastweek_start + ' - ' + str_lastweek_end
    msgText = MIMEText("""    <h4>Hi,</h4>
    <p>We have updated the website!</p>
    <p>參考日期:"""+ period + """</p>
    <div><img src="cid:image1" height="600" width="600"></div>
    <p>文章列表</p>
    <ul>%s"""% (week_list,) + """</ul>
    <br/>
    <p>""" + keyword + """  相關文章:</p>
    <div>
    <ul>%s</ul>
    <br />
    <h3>Best Regard</h3></div>""" % (inserted_list,),'html','utf-8') 
    
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = 'Fubon Word Cloud' 
    msgRoot.attach(msgText)
    fp = open('static/img/weekly.jpg','rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage)
    
    smtp.sendmail(sender, addr, msgRoot.as_string())


# In[5]:


#月
def content3(addr, keyword):
    keywords = [x.strip() for x in keyword.split(',')]
    lis = []
    lilink = []
    lititle = c.execute("""SELECT title FROM News WHERE dt >= ? AND dt <= ? """,(str_lastmonth_start,str_lastmonth_end)).fetchall()
    for k in keywords:
        for l in lititle:
            if k in l:
                if l not in lis:
                    lis.append(l)
                    link = c.execute("""SELECT link FROM News WHERE title = ? """,(l,)).fetchone()
                    lilink.append(link)
            else:
                t = c.execute("""SELECT summary FROM News WHERE title = ? """,(l,)).fetchone()
                if k in t:
                    if l not in lis:
                        lis.append(l)
                        link = c.execute("""SELECT link FROM News WHERE title = ? """,(l,)).fetchone()
                        lilink.append(link)
    di = list()
    for e in range(0, len(lis)):
        k = '</li>' + lis[e] + ' : <br />' + lilink[e]
        di.append(k)
    inserted_list = '</li>'.join([x.strip() for x in di])
    
    monthi = list()
    monthtitle = c.execute("""SELECT title FROM WebCrawler  WHERE dt > ? AND dt < ? ORDER BY countMsg DESC LIMIT 10""",(stamp_lastmonth_start,stamp_lastmonth_end)).fetchall()
    monthlink = c.execute("""SELECT link FROM WebCrawler  WHERE dt > ? AND dt < ? ORDER BY countMsg DESC LIMIT 10""",(stamp_lastmonth_start,stamp_lastmonth_end)).fetchall()
    monthlist = list()
    for e in range(0, len(monthtitle)):
        k = '</li>' + monthtitle[e] + ' : <br/>' + monthlink[e]
        monthi.append(k)
    month_list = '</li>'.join([x.strip() for x in monthi])
    
    period = str_lastmonth_start + ' - ' + str_lastmonth_end
    msgText = MIMEText("""    <h4>Hi,</h4>
    <p>We have updated the website!</p>
    <p>參考日期:"""+ period + """</p>
    <div><img src="cid:image1" height="600" width="600"></div>
    <p>文章列表</p>
    <ul>%s"""% (month_list,) + """</ul>
    <br/>
    <p>""" + keyword + """  相關文章:</p>
    <div>
    <ul>%s</ul>
    <br />
    <h3>Best Regard</h3></div>""" % (inserted_list,),'html','utf-8')
    
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = 'Fubon Word Cloud' 
    msgRoot.attach(msgText)
    fp = open('static/img/monthly.jpg','rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage)
    
    smtp.sendmail(sender, addr, msgRoot.as_string())


# In[6]:


smtp = smtplib.SMTP('localhost',25)
tday = datetime.today()

reciever = c.execute("""SELECT Email FROM newsub WHERE Cycle = 1 """).fetchall()
for r in reciever:
    keyword = c.execute("""SELECT Keyword FROM newsub WHERE Email = ? """,(r,)).fetchone()
    content1(r, keyword)


# In[9]:


if tday.weekday() == 0:
    reciever = c.execute("""SELECT Email FROM newsub WHERE Cycle = 2 """).fetchall()
    for r in reciever:
        keyword = c.execute("""SELECT Keyword FROM newsub WHERE Email = ? """,(r,)).fetchone()
        content2(r, keyword)
        
if tday.day == 1:
    reciever = c.execute("""SELECT Email FROM newsub WHERE Cycle = 3 """).fetchall()
    for r in reciever:
        keyword = c.execute("""SELECT Keyword FROM newsub WHERE Email = ? """,(r,)).fetchone()
        content3(r, keyword)

