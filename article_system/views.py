from django.shortcuts import render,HttpResponse
from .models import *
from .forms import Article_Form

def create_article(request):
    if request.method == 'POST':
        form = Article_Form(request.POST,request.FILES)
        if form.is_valid():
            article_record = form.save(commit=False)
            if request.user.is_authenticated:
                article_record.creator=request.user
            article_record.save()
        return HttpResponse('Article creation success')
    else:
        form = Article_Form()
        return render(request, 'create_article.html', {'form':form})