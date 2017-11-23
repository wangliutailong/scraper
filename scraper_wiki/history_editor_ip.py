from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import re
import json
from urllib import error

random.seed(datetime.datetime.now())

def getLinks(articleUrl):
    html = urlopen("http://en.wikipedia.org"+articleUrl)
    bsObj = BeautifulSoup(html)
    return bsObj.find("div",{"id":"bodyContent"}).findAll("a",href=re.compile("(/wiki/)((?!:).)*$"))

def getHistoryIPs(pageUrl):
    pageUrl = pageUrl.replace("/wiki/","")
    historyUrl = "https://en.wikipedia.org/w/index.php?title="+pageUrl+"&action=history"
    print("History url is: " + historyUrl)
    try:
        html = urlopen(historyUrl)
        bsObj = BeautifulSoup(html)
        ipAddresses = bsObj.findAll("a",{"class":"mw-userlink mw-anonuserlink"})
        addressList = set()
        for ipAddresse in ipAddresses:
            addressList.add(ipAddresse.get_text())
        return addressList
    except error.URLError:
        return []


def getCountry(ipAddress):
    try:
        response = urlopen("http://freegeoip.net/json/" + ipAddress).read().decode('utf-8')
    except error.URLError:
        return None
    responseJson = json.loads(response)
    return responseJson.get("country_code")

#print(getCountry("202.53.87.74"))

links = getLinks("/wiki/Python_(programming_language)")

countryCnt = {}

# for i in range(15):
#     link = links[i]
for link in links:
    print("-------------------")
    historyIPs = getHistoryIPs(link.attrs["href"])
    for historyIP in historyIPs:
        country = getCountry(historyIP)
        if country is not None:
            print(historyIP + " is from " + country)
            if country in countryCnt:
                countryCnt[country] += 1
            else:
                countryCnt[country] = 1
        else:
            print(historyIP)

print("\n")
for (k,v) in countryCnt.items():
    print("[\"" + str(k) + "\"," + str(v) + "],")

