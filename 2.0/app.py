
# coding: utf-8

# In[32]:


from flask import Flask ,render_template, jsonify, g, request, redirect, send_file
import json
import sqlite3 as lite
from datetime import datetime,timedelta ,date,time

from SqliteData import index_data, tag_data, gChart_data,wdCloud_data,keywordsearch,normalnews,generateword

con = lite.connect('../FBWEB.sqlite')
c = con.cursor()

app = Flask(__name__)


# In[33]:


#ok
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


# In[34]:


#ok
@app.route('/Awordcloud', methods=['GET', 'POST'])
def AwordCloud():
    if request.method == 'POST':
        #result = request.form.get('freqOption')
        start = request.form.get('start')
        end = request.form.get('end')
        print(start,end)
        cloud=wdCloud_data(start,end)
        date = start + '-' + end

        return render_template('Awordcloud.html',date = date,cloud = cloud)
    else:
        end = datetime.today()
        #start = start + timedelta(-1)
        start = end + timedelta(-1)
        end = datetime.strftime(end,'%Y-%m-%d')
        start = datetime.strftime(start,'%Y-%m-%d')
        #print(start)
        cloud=wdCloud_data(start,end)
        date = start + '-' + end
        return render_template('Awordcloud.html',date = date,cloud = cloud)


# In[35]:


#ok
@app.route('/Acharts', methods=['GET', 'POST'])
def Acharts():
    #get the data that google chart need
    #1=day 2=week 3=month
    dayChart=gChart_data(1)
    weekChart=gChart_data(2)
    monthChart=gChart_data(3)
    return render_template('Acharts.html', dayChart=dayChart, weekChart=weekChart, monthChart=monthChart)


# In[36]:


#ok
@app.route('/Arelwords', methods=['GET', 'POST'])
def Arelword():
    return render_template('Arelwords.html')


# In[37]:


#ok
@app.route('/AsubUs', methods=['GET', 'POST'])
def AsubUs():
    error = ''
    try:
        if request.method == 'POST':
            user =  request.form['email']
            cycle = request.form['cycle']
            keyword = request.form['keyword']
            c.execute("""INSERT INTO newsub(Email, Cycle, Keyword) VALUES(?,?,?)""",(user,cycle,keyword,))
            con.commit()
            return render_template("AsubUs.html",error = error)
        else:
            return render_template("AsubUs.html", error = error)
    except Exception as e:
        error = "Invalid"
        return render_template("AsubUs.html", error = error)


# In[38]:


@app.route('/BsetKeywords', methods=['GET', 'POST'])
def BsetKeywords():
    try:
        if request.method == 'POST':
            keywordstring = request.form.get('keyword')
            total, keywords = keywordsearch(keywordstring)
            return render_template("Bnews.html",total = total, keywords = keywords)
        else:
            return render_template("BsetKeywords.html")
    except Exception as e:
        return render_template("BsetKeywords.html")


# In[39]:


@app.route('/Bnews', methods=['GET', 'POST'])
def Bnews():
    total = normalnews()
    keywords =''
    return render_template('Bnews.html',total = total, keywords = keywords)


# In[40]:


@app.route('/BnewsWord', methods=['GET', 'POST'])
def BnewsWord():
    if request.method == 'POST':
        links = request.form.getlist('new_list')
        generateword(links)
        return send_file('/ods/analysis/J0235/2.0/富邦人壽新聞重點摘錄.docx')
    else:
        total = normalnews()
        keywords =''
        return render_template('BnewsWord.html', total = total, keywords = keywords)


# In[41]:


#ok
@app.route('/Akeyword/<string:words>/<int:freq>', methods=['GET', 'POST'])
def tag(words,freq):
    d_tag=tag_data(words,freq)
    return render_template('Akeyword.html',words=words,data=d_tag)


# In[42]:


if __name__ == '__main__':
    app.run(host = "10.42.71.210",port = 5001)

