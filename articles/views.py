from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm, CommentForm
from .models import Article, Comment
from IPython import embed
# from django.db.models import Q
from django.db.models import Count
from django.contrib.auth import get_user_model

# Create your views here.
def index(request):
    like = request.GET.get('like')
    view = request.GET.get('view')
    time = request.GET.get('time')
    if like:
        articles = Article.objects.annotate(like_count=Count('like_users')).order_by('-like_count')
    elif view:
        articles = Article.objects.all().order_by('-views')
    elif time:
        articles = Article.objects.all().order_by('-created_at')
    else:
        articles = Article.objects.all()

    context = {
        'articles': articles
    }
    return render(request, 'articles/index.html', context)

@login_required
def create(request):
    if request.method=='POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            if article.image:
                article.image = request.FILES['image']
            article.save()
            return redirect('articles:index')
    else:
        form = ArticleForm()
    context = {
        'form': form
    }
    return render(request, 'articles/form.html', context)

def detail(request, id):
    article = get_object_or_404(Article, id=id)
    article_form = ArticleForm(instance=article)
    article = article_form.save(commit=False)
    article.views = article.views + 1
    article.save()
    form = CommentForm()
    # cnt = Like.objects.filter(article=article).count()
    context = {
        'article': article,
        'form': form,
        # 'cnt': cnt,
    }
    return render(request, 'articles/detail.html', context)

def mypage(request, id):
    user = get_object_or_404(get_user_model(), id=id)
    articles = Article.objects.filter(user=user)
    comments = Comment.objects.filter(user=user)
    context = {
        'articles': articles,
        'comments': comments
    }
    return render(request, 'articles/mypage.html', context)

def update(request, id):
    article = get_object_or_404(Article, id=id)
    if request.method=='POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            if request.FILES.get('image'):
                article.image = request.FILES['image']
            article.save()
            return redirect('articles:detail', id)
    else:
        form = ArticleForm(instance=article)
    context = {
        'form': form
    }
    return render(request, 'articles/form.html', context)

def delete(request, id):
    article = get_object_or_404(Article, id=id)
    article.delete()
    return redirect('articles:index')

def comment_create(request, id):
    if request.method=='POST':
        article = get_object_or_404(Article, id=id)
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.user = request.user
            if request.FILES.get('image'):
                comment.image = request.FILES['image']
            comment.save()
    return redirect('articles:detail', id)

def comment_delete(request, article_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return redirect('articles:detail', article_id)

def search(request):
    if request.GET.get('keyword'):
        search_type = 'contains'
        articles = Article.objects.filter(title__contains=request.GET.get('keyword')).order_by('-created_at')
        articles2 = Article.objects.filter(content__contains=request.GET.get('keyword')).order_by('-created_at')
        return render(request, 'articles/search.html', {'articles': articles, 'articles2': articles2})
    else:
        return redirect('articles:index')

def like(request, id):
    article = get_object_or_404(Article, id=id)
    user = request.user
    if article.like_users.filter(id=user.id):
        article.like_users.remove(user)
    else:
        article.like_users.add(user)
    # if Like.objects.filter(article=article, user=user):
    #     like = get_object_or_404(Like, user=request.user)
    #     like.delete()
    # else:
    #     like = Like()
    #     like.user = request.user
    #     like.article = article
    #     like.save()
    return redirect('articles:detail', id)