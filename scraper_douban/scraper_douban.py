from snownlp import SnowNLP
import matplotlib.pyplot as plt
import re
import requests
import csv
import random
import codecs
import time
import datetime
from bs4 import BeautifulSoup

def save_comment_data(soup, file):
    csvfile = open(file,'a',newline="")
    writer = csv.writer(csvfile)
    for cm in soup.find_all("div", {"class": "comment"}):

        try:
            user = cm.find("", {"class": "comment-info"}).find("a").get_text().strip()
        except:
            user = ""
        try:
            vote = cm.find("", {"class": "votes"}).get_text().strip()
        except:
            vote = ""
        try:
            rate = cm.find("", {"class": re.compile("^allstar(\d)+ rating$")})["title"].strip()
            # rate = cm.find("",{"class":"allstar10 rating"})["title"]
        except:
            rate = ""
        try:
            time = cm.find("", {"class": "comment-time"}).get_text().strip()
        except:
            time = ""
        try:
            content = cm.p.get_text().strip()
        except:
            content = ""
        #print("-" * 50)
        #print("user: %s, vote: %s, rate: %s, time: %s." % (user, vote, rate, time))
        try:
            writer.writerow([user,vote,rate,time,content])
        except:
            pass

prefix = 'https://movie.douban.com/subject/26322642/comments'
first_url = "https://movie.douban.com/subject/26883064/comments"
header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Connection':'keep-alive'}

f_cookies = open('cookies.txt','r')
cookies = {}
for line in f_cookies.read().split(";"):
    name, value = line.strip().split("=",1)
    cookies[name] = value
    #print("%s = %s" % (name, value))

#clear data.csv
f = open("data.csv","w")
f.close()
html = requests.get(first_url,cookies=cookies,headers=header).content
soup = BeautifulSoup(html,"lxml")
save_comment_data(soup, "data.csv")
next_page = soup.findAll("a",{"class":"next"})

print(next_page)
print(next_page[0].attrs["href"])

i = 1
while (next_page != []):
    time.sleep(1 + float(random.randint(1, 100)) / 20)
    next_url = prefix + next_page[0].attrs["href"]
    html = requests.get(next_url, cookies=cookies, headers=header).content
    soup = BeautifulSoup(html, "lxml")
    save_comment_data(soup, "data.csv")
    next_page = soup.findAll("a", {"class": "next"})
    print("loop i = %d" % i)
    i += 1



csvf = open("data.csv","r")
reader = csv.reader(csvf)


sentiments = []
rate = []
for row in reader:
    s = SnowNLP(row[4])
    sentiments.append(s.sentiments)
    if(row[2] == "很差"):
        rate.append(1)
    elif(row[2] == "较差"):
        rate.append(2)
    elif (row[2] == "还行"):
        rate.append(3)
    elif (row[2] == "推荐"):
        rate.append(4)
    else:
        rate.append(5)


plt.title("sentiments distribution (simple size %d)" % len(sentiments))
plt.xlabel("sentiment evaluate")
plt.ylabel("number of people")
plt.hist(sentiments,bins=10)
plt.show()

print(rate)

plt.title("User rate (simple size %d)" % len(sentiments))
plt.xlabel("Score")
plt.ylabel("number of people")
plt.hist(rate,bins=5)
plt.show()


