from django.shortcuts import render,redirect
from django.views import View
from django.contrib import messages

from .forms import ArticleForm
from .models import Article
from .preprocessing_pipeline import Preprocess
from .scrapper import (
    ScrapeArticleURL, ArticlesFromKeywords
)

import pandas as pd
# Create your views here.

def renderHomeView(request,buffer):
    return render(
            request,
            "dashboard.html",{
                "form":ArticleForm,
                "buffer":buffer
        })

class ArticleView(View):
    form_class = ArticleForm
    template_name = "dashboard.html"

    def get(self,request):
        form = self.form_class()
        return renderHomeView(request,False)

    def post(self,request):
        form = self.form_class(request.POST)

        if form.is_valid():
            corpus_url = form.cleaned_data['corpus_url']
            articleResponse = ScrapeArticleURL(corpus_url)
            print("[+] %s successfully fetched " % (corpus_url))

            current_article = Article.objects.create(
                corpus_url=corpus_url,corpus_title=articleResponse['title'],
                corpus_text=articleResponse['body']
            )
            
            df_article = ArticlesFromKeywords(articleResponse['keywords'])
            
            if df_article is None:
                messages.error(request,"Unable to get any labels for the url")
                return renderHomeView(request,True)

            prepocess = Preprocess(df=df_article)
            prepocess.preprocess()
            df_article = prepocess.fetch_df()

            print("[+]Pre-processing of the corpus is done")


            return renderHomeView(request,True)