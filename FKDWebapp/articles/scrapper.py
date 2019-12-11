from newspaper import Article

from .GNews import GNews
from .models import Article as ArticleModel
from .models import ScrapeArticle

import pandas as pd 
import urllib3

def ScrapeArticleURL(url):
    """
    Segments a given article into a dictionary using url
    """
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

def ArticlesFromKeywords(user_url,ls_Keywords):
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
            return None, None

        urls = gnews_object.getlink()

        article_model_obj = ArticleModel.objects.get(corpus_url=user_url)
        ScrapeArticle.objects.bulk_create([
            ScrapeArticle(article=article_model_obj,scrape_url=url) for url in urls
        ])
        
        #Scrapes the articles for text and title from obtained links
        article_title = []
        article_text = []
        article_summary = []
        urlResponse = ""
        for url in urls:
                try:
                    article = Article(url,language="en")
                    article.download()
                    article.parse()
                    article.nlp()
                    article_title.append(article.title)
                    article_text.append(article.text)
                    article_summary.append(article.summary)
                    urlResponse += "[+] URL fetched: {}\n".format(url)
                except:
                    urlResponse += "[+] URL not fetched: {}\n".format(url)

        article_info = [article_title,article_text,article_summary]
        df = pd.DataFrame(article_info)
        df = df.transpose()
        df.columns = ["title","body","summary"]
        print("urlResponse:",urlResponse)
        return [df,urlResponse]
