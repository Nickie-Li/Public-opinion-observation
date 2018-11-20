
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
from apyori import apriori
from datetime import datetime,timedelta
import time
import random
import networkx as nx
#import graph_objs as go
import numpy as np
from PIL import Image
from os import path
import math


# In[2]:


connect = sqlite3.connect('../FBWEB.sqlite')
c = connect.cursor()
c.row_factory = lambda cursor, row: row[0]
con = connect.cursor()


# #Create Table
# c.execute("""DROP TABLE Apriori""")
# c.execute("""CREATE TABLE Apriori (Id integer PRIMARY KEY AUTOINCREMENT,Date datetime)""")
# for item in range(1,16):
#     column_name = str(item)
#     #print(column_name)
#     c.execute("""ALTER TABLE Apriori ADD '{}' char(10)""".format(column_name))
# 
# #pra = con.execute("""PRAGMA TABLE_INFO(Apriori)""").fetchall()
# #pra

# In[29]:


#get yesterday record
today = datetime.now()
today = datetime.strftime(today,'%Y-%m-%d')
#today = '2018-06-24'
todaydata = c.execute("""SELECT DISTINCT(words) FROM WordsCount WHERE daytime = ? ORDER BY wordsCount DESC LIMIT 15""",(today,)).fetchall()
#print(yesdata)
c.execute("""INSERT INTO Apriori(Date) VALUES(?)""",(today,))
r = list()
for i in todaydata:
    r.append(i)
#print(r)
count = 1
for t in r:
    sc = str(count)
    con.execute('''UPDATE Apriori SET '{}' = (?) WHERE Date = (?)'''.format(sc),(t,today,))
#     con.execute('''UPDATE Apriori SET '{}' = (?) WHERE DateTime = (?)'''.format(sc),(t,kday,))
    count = count + 1

f = con.execute("""SELECT * FROM Apriori""").fetchall()
#print(f)
connect.commit()


# In[30]:


#f = con.execute("""DELETE FROM Apriori WHERE Id = 14""").fetchall()
#connect.commit()
#f = con.execute("""SELECT * FROM Apriori WHERE Id = 24""").fetchall()


# In[32]:


dataset = pd.read_sql_query(("""SELECT * FROM Apriori"""),connect)
ds = dataset.loc[:, dataset.columns != 'Id']
df = ds.loc[:, ds.columns != 'Date']
#dataset


# In[33]:


transaction = []
coun = c.execute("""SELECT Count(ID) FROM Apriori""").fetchall().pop()
for i in range(0,coun):
    transaction.append([str(df.values[i,j]) for j in range(1,15)])


# In[41]:


minlift = coun / 2
#minlift


# In[73]:


rules = apriori(transaction,min_support = 0.001,min_confidence = 0.06,min_lift = minlift,min_length = 1,max_length = 2)


# In[74]:


counter = 1
w1 = list()
w2 = list()
conf = list()
lif = list()
sup = list()
for result in rules:
    #print(result)
    word1 = next(iter(result.items))
    w1.append(word1)
    #print(next(iter(result.items)))
    word2 = next(iter(result.ordered_statistics[0].items_add))
    if(word2 != word1):
        w2.append(word2)
    else:
        word2 =next(iter(result.ordered_statistics[0].items_base))
        w2.append(word2)
    #print(next(iter(next(iter(result.ordered_statistics[1])))))
    #print(word2)
    confidence = result.ordered_statistics[0].confidence
    conf.append(confidence)
    #print(result.ordered_statistics[0].confidence)
    lift = result.ordered_statistics[0].lift
    lif.append(lift)
    #print(result.ordered_statistics[0].lift)
    supportvalue = result.support
    sup.append(supportvalue)
    counter = counter + 1
    if(counter > 1000):
        break;
#print(lift)
dt = pd.DataFrame({'1' : w1,'2' : w2,'confidence' : conf,'support' : sup,'lift' : lif})
#dt


# In[75]:


def search(word):
    for count in range(0,len(test)):
        if(word == test[count]):
            return False
    return True


# In[76]:


test = list()
for k in w1:
    flag = search(k)
    if(flag and k != 'None' and k != '000'):
        #print(k)
        test.append(k)

                
for i in w2:
    flag = search(i)
    if(flag and i != 'None' and i != '000'):
        test.append(i)
        #print(i)

#test


# In[77]:


lift_edge = {}
p = 0
for i in range(0,len(test)-1):
    front = test[i]
    p = p + 1
    for j in range(p,len(test)):
        back = test[j]
        index1 = front + back
        index2 = back + front
        for count in range(0,len(w1)):
            i = w1[count]+w2[count]
            if(index1 == i):
                lift_edge[index1] = lif[count]
            elif(index2 == i):
                lift_edge[index1] = lif[count]

#lift_edge


# In[78]:


def draw_graph(): 

    G1 = nx.Graph()
    webc = '../2.0/static/img'
    c = 0
    flag = 0
    for count in range(0,len(test)-1):
        w = test[count]
        G1.add_node(w)
        c = c + 1
        for i in range(c,len(test)):
            index = test[count] + test[i]
            for ic in range(0,len(w1)):
                str1 = w1[ic]+w2[ic]
                str2 = w2[ic]+w1[ic]
                if(index == str1):
                    liftvalue = lift_edge[str1]
                    #print(index + ':' + '?',liftvalue)
                    #liftvalue = (1 / liftvalue *100) ** 3 / 10
                    if(liftvalue > 0 and liftvalue < coun):
                        liftvalue = 100
                    elif(liftvalue >= coun):
                        liftvalue = 600
                    G1.add_edge(test[count], test[i], length = liftvalue)
                elif(index == str2):
                    liftvalue = lift_edge[str2]
                    #print(index + ':' + '?',liftvalue)
                    #liftvalue = (1 / liftvalue *100) ** 3 / 10
                    if(liftvalue > 0 and liftvalue < coun):
                        liftvalue = 100
                    elif(liftvalue >= coun):
                        liftvalue = 600
                    G1.add_edge(test[count], test[i], length = liftvalue)


    edges = G1.edges()        
#    print(c)
    colors = 'black'
    weights = 1
    pos = nx.spring_layout(G1,k=0.15,iterations=10)

    n = nx.draw(G1, pos, font_path='../msyh.ttf', node_color = 'skyblue', node_size = 300, edge_color = colors, width = weights ,length = liftvalue, font_size = 6, with_labels = True ,height = 20,)            
#    for p in pos:  # raise text positions
#        pos[p][1] += 0.05
#    nx.draw_networkx_labels(G1, pos)
#    plt.figure(figsize=(8,8))  

#    plt.xlim(-1.0,1.0)
#    plt.ylim(-1.0,1.0)
    plt.axis('off') 
    plt.savefig("../2.0/static/img/Graph.png", format="PNG", dpi=1000)
    #plt.show()

draw_graph()

