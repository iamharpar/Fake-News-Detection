from newspaper import Article
from .GNews import GNews

import pandas as pd 
import urllib3

def ScrapeArticleURL(url):
    article = Article(url,language="en")
    article.download()
    article.parse()
    article.nlp()
    
    article_title = article.title
    article_text = article.text
    article_keywords = article.keywords
    

    return {
        "title":article_title,
        "body":article_text,
        "keywords":article_keywords,
        "summary":article.summary
    }

def ArticlesFromKeywords(ls_Keywords):
        """
        Function takes in a list of keywords and searches 
        on google news for similar articles scrapes them and returns
        a dictionary containing the article text and title.
        """

        #obtains the link of news articles having similar keywords
        gnews_object = GNews()
        gnews_object.search(ls_Keywords)
        gnews_response = gnews_object.getpage()
        if gnews_response is None:
            return None

        urls = gnews_object.getlink()

        #Scrapes the articles for text and title from obtained links
        article_title = []
        article_text = []
        article_summary = []
        for url in urls:
                try:
                    article = Article(url,language="en")
                    article.download()
                    article.parse()
                    article.nlp()
                    article_title.append(article.title)
                    article_text.append(article.text)
                    article_summary.append(article.summary)
                    print("[+] URL fetched: {}".format(url))
                except:
                    print("[+] URL not fetched: {}".format(url))
        article_info = [article_title,article_text,article_summary]
        df = pd.DataFrame(article_info)
        df = df.transpose()
        df.columns = ["title","body","summary"]
        return df
