import aiohttp
import asyncio

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
                response_data = None
        return response_data
    
    def getRawDataResponse(self,dict_response=False):
        try:
            futures = [self.__fetch_url(u) for u in self.keyword_url]
            response,_ = self.__loop.run_until_complete(asyncio.wait(futures))
        finally:
            self.__loop.close()

        response = [res.result() for res in response]
        if dict_response:
            return dict(zip(self.search_q,response))
        return response


'''
URL  = ['mark','google','earth','apple','bing','steve','earth','fbi','james comey']
news = NewsURLScrapper(search_q=URL)
res = news.getRawDataResponse(dict_response=True)
'''