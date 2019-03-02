from django.db import models
from django.core.validators import URLValidator

# Create your models here.

class Article(models.Model):
    PREDICITIONS = (
        ("FAKE","Fake"),
        ("REAL","Real"),
        ("NA","Not sure"),
    ) 

    corpus_url = models.URLField(validators=[URLValidator])
    corpus_title = models.TextField()
    corpus_text = models.TextField(blank=True,null=True)
    model_status = models.CharField(max_length=10,choices=PREDICITIONS)
    
    time = models.TimeField(auto_now=True)

    def __str__(self):
        return self.corpus_title
    
    def __unicode__(self):
        return self.corpus_title

    

