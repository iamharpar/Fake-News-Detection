from django import forms
from .models import Article
#create forms here ... 

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('corpus_url',)
    
    def __init__(self,**kwargs):
        corpus_url = forms.URLInput()
        super(ArticleForm,self).__init__(**kwargs)
    