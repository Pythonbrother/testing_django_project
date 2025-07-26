import random,json,datetime
from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse, HttpResponse
from .models import *
from .forms import Article_Form
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy,reverse
def create_article(request):
    if request.method == 'POST':
        form = Article_Form(request.POST,request.FILES)
        if form.is_valid():
            article_record = form.save(commit=False)
            if request.user.is_authenticated:
                article_record.creator=request.user
            article_record.save()
            new_pk = article_record.pk
        return redirect('article_detail',new_pk)
    else:
        form = Article_Form()
        return render(request, 'create_article.html', {'form':form})

def article_intro(request):
    if request.method == 'POST':
        search_value = request.POST.get('name_search')
        record = get_object_or_404(Article, name=search_value)
        return redirect('article_detail', record.pk)
    else:
        all_records = Article.objects.values('name','caption')
        twelve_random_num_from_articles_model = random.sample(list(Article.objects.values_list('id',flat=True)),12)
        twelve_random_articles = Article.objects.filter(id__in=twelve_random_num_from_articles_model)
        return render(request, 'article_intro_page.html', {'random_articles':twelve_random_articles,'all_records':all_records})

def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    full_comments = Comment_to_Article.objects.filter(article=article).select_related('commenter').order_by('-created_time')
    comment_data = [{
        'comment_pk': comment.pk,
        'commenter': comment.commenter.username,
        'comment': comment.comment,
        'replies': [{'comment':replie.comment,'commenter':replie.commenter.username} for replie in Comment_to_Comment.objects.filter(
            target_comment=comment.pk)],
        'upload_at': comment.created_time.strftime("%Y-%m-%d"),
    } for comment in full_comments]

    if request.method == 'GET':
        return render(request, 'article_detail.html', {'article_record': article,'comment_data':json.dumps(comment_data)})
    else:
        comment = request.POST.get("comment")
        if comment:
            Comment_to_Article.objects.create(comment=comment, article=article, commenter=request.user)
            full_comments = Comment_to_Article.objects.filter(article=article).select_related('commenter').order_by('-created_time')
            comment_data = [{
                'comment_pk':comment.pk,
                'commenter':comment.commenter.username,
                'comment':comment.comment,
                'replies':[{'comment':replie.comment,'commenter':replie.commenter.username} for replie in Comment_to_Comment.objects.filter(target_comment=comment.pk)],
                'upload_at':comment.created_time.strftime("%Y-%m-%d"),
            } for comment in full_comments]
            return JsonResponse({'comment_data': comment_data})
        replies_comment = request.POST.get("replies_comment")
        to_comment_pk = request.POST.get("to_comment_pk")
        target_comment = get_object_or_404(Comment_to_Article,pk=to_comment_pk)
        if replies_comment:
            Comment_to_Comment.objects.create(comment=replies_comment,target_comment=target_comment,commenter=request.user)
            comment_data = [{
                'comment_pk': comment.pk,
                'commenter': comment.commenter.username,
                'comment': comment.comment,
                'replies': [{'comment':replie.comment,'commenter':replie.commenter.username} for replie in Comment_to_Comment.objects.filter(target_comment=comment.pk)],
                'upload_at': comment.created_time.strftime("%Y-%m-%d"),
            } for comment in full_comments]
            return JsonResponse({'comment_data':comment_data})

class update_article(UpdateView):
    model = Article
    fields = ['name','caption','topic','photo']
    template_name = 'update_article.html'
    def get_success_url(self):
        return reverse('article_detail', kwargs={'article_pk': self.object.pk})

class delete_article(DeleteView):
    model = Article
    template_name = 'delete_article.html'
    success_url = reverse_lazy('article_intro')