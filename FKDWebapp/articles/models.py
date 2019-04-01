from django.db import models
from django.core.validators import URLValidator

# Create your models here.
class Article(models.Model):
    corpus_url = models.URLField(validators=[URLValidator])
    corpus_title = models.TextField()
    model_stance = models.CharField(max_length=10)
    model_prob = models.CharField(max_length=10)
    time = models.TimeField(auto_now=True)
    
    def __str__(self):
        return self.corpus_title
    
    def __unicode__(self):
        return self.corpus_title


class ArticleKeywords(models.Model):
    article = models.ForeignKey(Article,on_delete=models.CASCADE)
    keywords = models.CharField(max_length=10)
    
class ScrapeArticle(models.Model):
    article = models.ForeignKey(Article,on_delete=models.CASCADE)
    scrape_url = models.CharField(max_length=300)
