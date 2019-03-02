import re
import xml.etree.ElementTree as ET 
import aiohttp
import asyncio
import requests


'''
    search_q contains keywords regarding the news article 
    first generate set of URLS to be used. Make async request
    to these urls using grequests generator
'''
class NewsURLScrapper(object):
    GOOGLE_NEWS_URL = "https://news.google.com/rss/search?q={}&hl=en-IN&gl=IN&ceid=IN:en"
    getGoogleUrl = lambda x : NewsURLScrapper.GOOGLE_NEWS_URL.format(x)
    
    def __init__(self, search_q):
        self.search_q = search_q
        assert type(self.search_q) is list
        self.__loop = asyncio.get_event_loop() 
        self.keyword_url = [NewsURLScrapper\
            .getGoogleUrl(u) for u in self.search_q]

    async def __fetch_url(self,url):
        async with aiohttp.ClientSession(loop=self.__loop) as client:
            try:
                async with client.get(url) as response:
                    response_data = await response.text()
            except:
                response_data = await None
        return response_data
    
    def getRawDataResponse(self,dict_response=False):
        try:
            futures = [self.__fetch_url(u) for u in self.keyword_url]
            response,_ = self.__loop.run_until_complete(asyncio.wait(futures))
        finally:
            self.__loop.close()

        response = [res.result() for res in response]
        if dict_response:
            response = dict(zip(self.search_q,response))
            return {k: v for k, v in response.items() if v is not None}
        return response

class GetNewsArticle(NewsURLScrapper):
    def __init__(self, search_q):
        super(GetNewsArticle, self).__init__(search_q)
    
    def sanitizeResponseURL(self):
        response = self.getRawDataResponse(dict_response=True)

        if not len(response):
            print("empty dict")
            return

        for res,data in response.items():
            tree = ET.parse(data)
            print(tree)
            print(tree.getroot())


news = GetNewsArticle(search_q=['google'])        
news = news.sanitizeResponseURL()
