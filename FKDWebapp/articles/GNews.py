import bs4
from bs4 import BeautifulSoup as soup
import urllib.request as GNewsRequests

class GNews(object):
        def __init__(self):
                self.texts = []
                self.links = []
                self.results = []
                self.key = ""

        def search(self, keys):
                for single_key in keys:
                    self.key = self.key + single_key + "+"
                    self.key = self.key.replace(" ","+")
                self.getpage()

        def getpage(self, page=1):
                self.user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0'
                self.headers = {'User-Agent':self.user_agent}
                self.url = "https://www.google.com/search?q="+self.key+"&tbm=nws&start=%d" % (10*(page-1)) 
                self.req = GNewsRequests.Request(self.url, headers=self.headers)
                self.response = GNewsRequests.urlopen(self.req)
                self.page = self.response.read()
                
                self.content = soup(self.page, "html.parser")
                try:
                        result = self.content.find(id="rso").find_all("div", class_="g")
                except:
                        return None

                for item in result:
                        try:
                                self.texts.append(item.find("h3").text)
                                self.links.append(item.find("h3").find("a").get("href"))
                                self.results.append({
                                'title':item.find("h3").text,
                                'media':item.find("div", class_="slp")\
                                        .find_all("span")[0].text,
                                'date':item.find("div", class_="slp")\
                                        .find_all("span")[2].text,
                                'desc':item.find("div", class_="st").text,
                                'link':item.find("h3").find("a").get("href"),
                                'img':item.find("img").get("src")
                        })
                        except:
                                print("[-]Provided url does not belong to a News Website")
                self.response.close()
                return self.results

        def result(self):
                return self.results

        def gettext(self):
                return self.texts

        def getlink(self):
                return self.links

        def clear():
                self.texts = []
                self.links = []
                self.results = []
