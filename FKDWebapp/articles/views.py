from django.shortcuts import render
from django.views import View
from .forms import ArticleForm
# Create your views here.

class ArticleView(View):
    def get(self,request):
        return render(
            request,
            "dashboard.html",{
                "form":ArticleForm,
                "debug":False
            }
        )

    def post(self,request):
        return render(
            request,
            "dashboard.html",{
                "form":ArticleForm,
                "debug":True
            }
        )
    
