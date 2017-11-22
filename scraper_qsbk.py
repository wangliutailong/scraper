import urllib
import urllib2
import cookielib
import re
from bs4 import BeautifulSoup

class QSBK:
    def __init__(self):
        self.pageIndex = 1
        self.user_agent =  'Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'
        self.headers = {'User-Agent':self.user_agent}
        self.stories = []
        self.enable = True
    def getPage(self, page_index):
        try:
            url = 'https://www.qiushibaike.com/hot/page/' + str(page_index)
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            soup = BeautifulSoup(response.read().decode('utf-8'),"lxml")
            return soup
        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print u"Connection failed", e.reason
            return None
    def getPageItems(self, pageIndex):
        soup = self.getPage(pageIndex)
        if not soup:
            print "Page loading failed"
            return None
        pageStories = []
        for duanzi in soup.find_all(class_=re.compile("article block untagged mb15")):
            author_name = duanzi.find(class_=re.compile("author")).find("h2").get_text().strip()
            content = duanzi.find(class_="content").get_text().strip()
            like = duanzi.find(class_="stats-vote").find(class_="number").get_text().strip()
            comment = duanzi.find(class_="stats-comments").find(class_="number").get_text().strip()
            pageStories.append([author_name, content,like,comment])
        return pageStories
    def loadPage(self):
        if self.enable == True:
            if len(self.stories) < 2:
                pageStories = self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1
    def getOneStory(self, pageStories, page):
        for story in pageStories:
            input = raw_input()
            self.loadPage()
            if input == "Q":
                self.enable = False
                return
            print u"Page:%s\t Author:%s\t like:%s\t comment:%s\n%s" % (page,story[0], story[2],story[3],story[1])
    def start(self):
        print u"Reading..."
        self.enable = True
        self.loadPage()
        nowPage = 0
        while self.enable:
            if len(self.stories)>0:
                pageStories = self.stories[0]
                nowPage += 1
                del self.stories[0]
                self.getOneStory(pageStories,nowPage)        
    
    
# page = 1
# url = 'https://www.qiushibaike.com/hot/page/' + str(page)
# user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'
# headers = {'User-Agent':user_agent}
# try:
#     request = urllib2.Request(url, headers=headers)
#     response = urllib2.urlopen(request)
#     soup = BeautifulSoup(response.read().decode('utf-8'),"lxml")
# except urllib2.URLError, e:
#     if hasattr(e,"code"):
#         print e.code
#     if hasattr(e,"reason"):
#         print e.reason

# for duanzi in soup.find_all(class_=re.compile("article block untagged mb15")):
#     author_content = duanzi.find(class_="content")
#     author_name = duanzi.find(class_=re.compile("author")).find("h2")
#     like = duanzi.find(class_="stats-vote").find(class_="number")
#     comment = duanzi.find(class_="stats-comments").find(class_="number")
#     print author_name.get_text().strip()
#     print author_content.get_text().strip()
#     print like.get_text().strip()
#     print comment.get_text().strip()
#     exit()

spider = QSBK()
spider.start()

