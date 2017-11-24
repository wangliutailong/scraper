import urllib
import urllib2
import cookielib
import re
from bs4 import BeautifulSoup

class BDTB:
    def __init__(self, baseUrl, seeLZ):
        self.pageIndex = 1
        self.baseURL = baseUrl
        self.seeLZ = 'see_lz=' + str(seeLZ)
        self.user_agent =  'Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'
        self.headers = {'User-Agent':self.user_agent}

    def getPage(self, pageNum):
        try:
            url = self.baseURL + "?" + self.seeLZ + "&pn=" + str(pageNum)
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            soup = BeautifulSoup(response.read().decode('utf-8'),"lxml")
            return soup
        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print u"Connection failed", e.reason
            return None

baseURL = 'http://tieba.baidu.com/p/3138733512'
spider = BDTB(baseURL,1)

soup=spider.getPage(1)
print soup.find(_class="core_title_txt")

for title in soup.findAll(class_=re.compile("core_title_txt")):
    print title.get_text()
