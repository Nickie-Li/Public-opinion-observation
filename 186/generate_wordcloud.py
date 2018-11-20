
# coding: utf-8

# In[106]:


from wordcloud import WordCloud, STOPWORDS

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import sqlite3
from os import path
import sys
import numpy as np
from PIL import Image


# In[107]:


connect = sqlite3.connect('../FBWEB.sqlite')
c = connect.cursor()
con = connect.cursor()
c.row_factory = lambda cursor, row: row[0] #add this line to get only value,not tuple


# In[124]:


from datetime import datetime,timedelta ,date,time
currentday = datetime.today()
yesterday = currentday + timedelta(-1)
yesterday = datetime.strftime(yesterday,'%Y-%m-%d')


weekday = currentday.date() + timedelta(-(currentday.weekday()))
weekday = datetime.strftime(weekday,'%Y-%m-%d')

monthday = currentday.date() + timedelta(-(currentday.day)+1)
monthday = datetime.strftime(monthday,'%Y-%m-%d')
currentday = datetime.strftime(currentday,'%Y-%m-%d')


# In[117]:


#a = con.execute("""SELECT * FROM WordsCount WHERE frequencyNum = 1""").fetchall()
#print(a)

# Daily

# In[118]:


word = c.execute("""SELECT words FROM WordsCount WHERE frequencyNum = 1 AND daytime = (?)""",(currentday,)).fetchall()
count = c.execute("""SELECT wordsCount FROM WordsCount WHERE frequencyNum = 1 AND daytime = (?)""",(currentday,)).fetchall()
di1 = {}
lw = list()
lc = list()
for insert in word:
    lw.append(insert)
    
for insert in count:
    lc.append(insert)
    
    
for e in range(0, len(lw)):
    k = lw[e]
    v = lc[e]
    di1[k] = v
    
#print(di1)


# In[119]:


# get path to script's directory
currdir = '../2.0/static/img'
webc = '../2.0/static/img'
d = path.dirname(__name__)
def create_wordcloud(text):
	# create numpy araay for wordcloud mask image
	masks = np.array(Image.open(path.join(webc, "Black_Circle.jpg")).convert('RGB'))

	# create set of stopwords	
	stopwords = set(STOPWORDS)

	# create wordcloud object
	wc = WordCloud(font_path='../msyh.ttf',background_color = "rgba(255, 255, 255, 0)", mode = "RGB",height = 20,width = 20,margin = 2,max_font_size=400,
					max_words=50, 
					mask=masks,
					stopwords=stopwords)
	wc.generate_from_frequencies(text)
	wc.to_file(path.join(currdir, "daily.jpg"))
	#wc.to_file(path.join(webc, "daily.jpg"))
	plt.imshow(wc, interpolation='bilinear')
	plt.axis('off')
#	plt.savefig('pink.jpg',dpi = 300)


if __name__ == "__main__":
	# get query
	query = sys.argv[1]
	text = di1
	create_wordcloud(text)


# Weekly

# In[122]:


word = c.execute("""SELECT words FROM WordsCount WHERE frequencyNum = 2 AND daytime = (?)""",(weekday,)).fetchall()
count = c.execute("""SELECT wordsCount FROM WordsCount WHERE frequencyNum = 2 AND daytime = (?)""",(weekday,)).fetchall()
di2 = {}
lw = list()
lc = list()
for insert in word:
    lw.append(insert)
    
for insert in count:
    lc.append(insert)
    
    
for e in range(0, len(lw)):
    k = lw[e]
    v = lc[e]
    di2[k] = v
    
#print(di2)


# In[123]:


# get path to script's directory
currdir = '../2.0/static/img'
webc = '../2.0/static/img'
d = path.dirname(__name__)
def create_wordcloud(text):
	# create numpy araay for wordcloud mask image
	masks = np.array(Image.open(path.join(webc, "Black_Circle.jpg")).convert('RGB'))

	# create set of stopwords	
	stopwords = set(STOPWORDS)

	# create wordcloud object
	wc = WordCloud(font_path='../msyh.ttf',background_color = "rgba(255, 255, 255, 0)", mode = "RGB",height = 20,width = 20,margin = 2,max_font_size=400,
					max_words=50, 
					mask=masks,
					stopwords=stopwords)
	wc.generate_from_frequencies(text)
	wc.to_file(path.join(currdir, "weekly.jpg"))
	#wc.to_file(path.join(webc, "weekly.jpg"))
	plt.imshow(wc, interpolation='bilinear')
	plt.axis('off')
#	plt.savefig('pink.jpg',dpi = 300)


if __name__ == "__main__":
	# get query
	query = sys.argv[1]
	text = di2
	create_wordcloud(text)


# Monthly

# In[131]:


word = c.execute("""SELECT words FROM WordsCount WHERE frequencyNum = 3 AND daytime = (?)""",(monthday,)).fetchall()
count = c.execute("""SELECT wordsCount FROM WordsCount WHERE frequencyNum = 3 AND daytime = (?)""",(monthday,)).fetchall()
lw = list()
lc = list()
di3 = {}
for insert in word:
    lw.append(insert)
    
for insert in count:
    lc.append(insert)
    
    
for e in range(0, len(lw)):
    k = lw[e]
    v = lc[e]
    di3[k] = v
    
#print(di3)


# # get path to script's directory
currdir = '../2.0/static/img'
webc = '../2.0/static/img'
d = path.dirname(__name__)
def create_wordcloud(text):
	# create numpy araay for wordcloud mask image
	masks = np.array(Image.open(path.join(webc, "Black_Circle.jpg")).convert('RGB'))

	# create set of stopwords	
	stopwords = set(STOPWORDS)

	# create wordcloud object
	wc = WordCloud(font_path='../msyh.ttf',background_color = "rgba(255, 255, 255, 0)", mode = "RGB",height = 20,width = 20,margin = 2,max_font_size=400,
					max_words=50, 
					mask=masks,
					stopwords=stopwords)
	wc.generate_from_frequencies(text)
	wc.to_file(path.join(currdir, "monthly.jpg"))
	#wc.to_file(path.join(webc, "monthly.jpg"))
	plt.imshow(wc, interpolation='bilinear')
	plt.axis('off')
#	plt.savefig('pink.jpg',dpi = 300)


if __name__ == "__main__":
	# get query
	query = sys.argv[1]
	text = di2
	create_wordcloud(text)

