from .scrapper import ArticlesFromKeywords,ScrapeArticleURL
from .preprocessing_pipeline import Preprocess
# Create your tests here.

df = ArticlesFromKeywords(['lok sabha','nda','congress','odisha'])
Preprocess(df).preprocess()