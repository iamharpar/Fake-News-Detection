from django import forms
from .models import Article
#create forms here ... 

class ArticleForm(forms.ModelForm):
    corpus_url = forms.URLInput()
    
    class Meta:
        model = Article
        fields = ('corpus_url',)