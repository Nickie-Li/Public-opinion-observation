import sqlite3 as lite
import jieba
import requests 
from bs4 import BeautifulSoup
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from datetime import datetime, timedelta ,date,time
import jieba.analyse as analyse
from dateutil.relativedelta import relativedelta


##日斷詞
def findlikeday():
    connection = lite.connect('../FBWEB.sqlite')
    connection.row_factory = lite.Row 
    summ = []
    today = datetime.today()
    today1 = datetime.strftime(today,'%Y-%m-%d')
    yesterday = today
    yesterday = datetime.strftime(yesterday,'%Y-%m-%d')
    yesterday1 = today + timedelta(-1)
    yesterday1 = datetime.strftime(yesterday1,'%Y-%m-%d')
    weekday = today.weekday()
    cursor = connection.execute("SELECT summary FROM webCrawler WHERE dt BETWEEN ? AND ? ",(yesterday1,yesterday,))
    for row in cursor:
        summ.append(row[0])
    return summ

def wordCount1():
    summ = findlikeday()
    summ = str(summ)
    words_ary = []
    stopWords = []
    today = datetime.today()
    today = datetime.strftime(today,'%Y-%m-%d')
    with open('stopWords.txt', 'r', encoding='UTF-8') as file:
        for data in file.readlines():
            data = data.strip()
            stopWords.append(data)
    
    with lite.connect('../FBWEB.sqlite')as conn:
        cur = conn.cursor()
        for word in jieba.cut(summ):
            words_ary.append(word)
        from collections import Counter
        words_ary = [word for word in jieba.cut(summ)]
        c = Counter(words_ary)
        hik ={}
        for k, v in c.most_common(100):
            if k in stopWords:
                continue
            else:
                if len(k) >= 2 and v >= 5:##k = 我、的(少於一個字的詞) V = 詞的最低數量
                    cur.execute("INSERT INTO wordsCount (words,wordsCount,daytime,frequencyNum)VALUES (?,?,?,?)", (k, v, today, 1))
                    hik[k]=hik.get(k,v)
                    
##週斷詞
def findlikeweek():
    connection = lite.connect('../FBWEB.sqlite')
    connection.row_factory = lite.Row 
    summ = []
    today = datetime.today()
    today1 = datetime.strftime(today,'%Y-%m-%d')
    yesterday = today
    yesterday = datetime.strftime(yesterday,'%Y-%m-%d')
    week = today + timedelta(-7)
    week = datetime.strftime(week,'%Y-%m-%d')
    weekday = today.weekday()
    if weekday == 0:
        cursor = connection.execute("SELECT summary FROM webCrawler WHERE dt BETWEEN ? AND ? ",(week,yesterday,))
        for row in cursor:
            summ.append(row[0])          
        return summ

def wordCount2():
    summ = findlikeweek()
    today = datetime.today()
    today = datetime.strftime(today,'%Y-%m-%d')
    summ = str(summ)
    words_ary = []
    stopWords = []
    today = datetime.today()
    today = datetime.strftime(today,'%Y-%m-%d')
    
    with open('stopWords.txt', 'r', encoding='UTF-8') as file:
        for data in file.readlines():
            data = data.strip()
            stopWords.append(data)
    
    with lite.connect('../FBWEB.sqlite')as conn:
        cur = conn.cursor()
        for word in jieba.cut(summ):
            words_ary.append(word)
        from collections import Counter
        words_ary = [word for word in jieba.cut(summ)]
        c = Counter(words_ary)
        hik ={}
        for k, v in c.most_common(100):
            if k in stopWords:
                continue
            else:
                if len(k) >= 2 and v >= 5:##k = 我、的(少於一個字的詞) V = 詞的最低數量
                    cur.execute("INSERT INTO wordsCount (words,wordsCount,daytime,frequencyNum)VALUES (?,?,?,?)", (k, v, today, 2))
                    hik[k]=hik.get(k,v) 
                    
##月斷詞
def findlikemonth():
    connection = lite.connect('../FBWEB.sqlite')
    connection.row_factory = lite.Row 
    summ = []
    today = datetime.today()
    today1 = datetime.strftime(today,'%Y-%m-%d')
    yesterday = today
    yesterday = datetime.strftime(yesterday,'%Y-%m-%d')
    month = datetime.strftime(today,'%d')
    week = today - relativedelta(months=1)
    week = datetime.strftime(week,'%Y-%m-%d')
    if month == '01':        
        cursor = connection.execute("SELECT summary FROM webCrawler WHERE dt BETWEEN ? AND ? ",(week,today1,))
        for row in cursor:
            summ.append(row[0])            
        return summ

def wordCount3():
    summ = findlikemonth()
    summ = str(summ)
    today = datetime.today()
    today = datetime.strftime(today,'%Y-%m-%d')
    words_ary = []
    stopWords = []
    today = datetime.today()
    today = datetime.strftime(today,'%Y-%m-%d')
    
    with open('stopWords.txt', 'r', encoding='UTF-8') as file:
        for data in file.readlines():
            data = data.strip()
            stopWords.append(data)
    
    with lite.connect('../FBWEB.sqlite')as conn:
        cur = conn.cursor()
        for word in jieba.cut(summ):
            words_ary.append(word)
        from collections import Counter
        words_ary = [word for word in jieba.cut(summ)]
        c = Counter(words_ary)
        hik ={}
        for k, v in c.most_common(100):
            if k in stopWords:
                continue
            else:
                if len(k) >= 2 and v >= 5:##k = 我、的(少於一個字的詞) V = 詞的最低數量
                    cur.execute("INSERT INTO wordsCount (words,wordsCount,daytime,frequencyNum)VALUES (?,?,?,?)", (k, v, today, 3))
                    hik[k]=hik.get(k,v)
                    print(k,v)



#findlikeday()
#wordCount1()
#findlikeweek()
#wordCount2()
findlikemonth()
wordCount3()