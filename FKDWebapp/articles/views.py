from django.shortcuts import render,redirect,HttpResponse
from django.views import View
from django.views.generic import ListView
from django.contrib import messages

from .forms import ArticleForm
from .models import Article,ScrapeArticle,ArticleKeywords
from .preprocessing_pipeline import Preprocess
from .model_pipline import ModelPipeline
from .scrapper import (
    ScrapeArticleURL, ArticlesFromKeywords
)

import time
import pandas as pd
# Create your views here.

class ArticleView(View):
    form_class = ArticleForm
    template_name = "dashboard.html"

    def get(self,request):
        form = self.form_class()
        return render(
            request,
            "dashboard.html",{
                "form":ArticleForm,
                "buffer":False
        })

    def post(self,request):
        form = self.form_class(request.POST)
        responseMsg = ""

        if form.is_valid():            
            corpus_url = form.cleaned_data['corpus_url']
            articleResponse = ScrapeArticleURL(corpus_url)
            print(articleResponse['keywords'])
            current_article = Article.objects.filter(corpus_url=corpus_url)
            
            if current_article:
                responseMsg = "*" * 5 + "[Cached Result]" + "*" * 5 + "\n"
                current_article = Article.objects.get(corpus_url=corpus_url)
                articleKeywords = ArticleKeywords.objects.filter(article=current_article)\
                    .values_list('keywords',flat=True)
                
                #print("[==> Fetched Keywords : ]",articleKeywords)
                tokenGen = "[==> Fetched Keywords : ] {}\n".format(articleKeywords)
                responseMsg += tokenGen

                fetched_urls = ScrapeArticle.objects.filter(article=current_article)\
                    .values_list('scrape_url',flat=True)    

                for u in fetched_urls:
                    currentFetch = "[+] Articles fetched from {}\n".format(u)
                    responseMsg += currentFetch
                    #print("[+] Articles fetched from %s " % (u))

                time.sleep(5)
                stanceResult = "\nGeneral trend {} with the article with the probability of {} percent".format(current_article.model_stance,current_article.model_prob)         
                responseMsg += stanceResult
                messages.success(request,"General trend  %s with the \
                        article with the probability of %s percent" %(
                    current_article.model_stance,
                    current_article.model_prob,
                ))

                response = HttpResponse(responseMsg,content_type="text/csv  ; charset=utf8")
                response['Content-Disposition'] = 'attachment; filename={}.csv'.format(current_article.corpus_title.replace(" ","-"))
                return response

            current_article = Article.objects.create(
                corpus_url=corpus_url,corpus_title=articleResponse['title'],
            )
            
            ArticleKeywords.objects.bulk_create([
                ArticleKeywords(article=current_article,keywords=w) for w in articleResponse['keywords']
            ])

            responseMsg += "[==> Fetched Keywords :{} ]\n".format(articleResponse['keywords'])
            
            df_scrape_article,urlResponse = ArticlesFromKeywords(corpus_url,articleResponse['keywords'])
            
            if df_scrape_article is None:
                messages.error(request,"Unable to get any labels for the url")
                return render(
                    request,
                    "dashboard.html",{
                        "form":ArticleForm,
                        "buffer":True
                    })

            responseMsg += urlResponse

            prepocess = Preprocess(df=df_scrape_article)
            prepocess.preprocess()
            df_scrape_article = prepocess.fetch_df()

            print("[+] Pre-processing for scrapped data completed")

            df_claim_article = pd.DataFrame([
                articleResponse['title'],articleResponse['body'],
                articleResponse['summary']
            ])
            df_claim_article = df_claim_article.transpose()
            df_claim_article.columns = ["title","body","summary"]

            print(df_claim_article.head())

            prepocess = Preprocess(df=df_claim_article)
            prepocess.preprocess()
            df_claim_article = prepocess.fetch_df()

            print("[+] Pre-processing for claim data completed")

            model_pipeline = ModelPipeline(df_scrape=df_scrape_article,df_claim=df_claim_article)
            predictions = model_pipeline.predict()

            current_article.model_stance = predictions[0]
            current_article.model_prob = predictions[1] * 100

            current_article.save()
            responseMsg += "\nGeneral trend {} with the article with the probability of {} percent".format(predictions[0],predictions[1]*100)
            messages.success(request,"General trend  %s with the article with the probability of %d percent" % (predictions[0],predictions[1]*100))

            response = HttpResponse(responseMsg,content_type="text/csv  ; charset=utf8")
            response['Content-Disposition'] = 'attachment; filename={}.csv'.format(current_article.corpus_title.replace(" ","-"))
            return response