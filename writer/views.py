from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import ArticleForm, UpdateUserForm
from .models import Article
from account.models import CustomUser
from django.db import IntegrityError
from django.core.exceptions import ValidationError


@login_required(login_url='my-login')
def writer_dashboard(request):
    return render(request, 'writer/writer-dashboard.html')


@login_required(login_url='my-login')
def create_article(request):
    if Article.objects.filter(user=request.user).exists():
        return render(request, 'writer/article-limit.html', status=403)

    form = ArticleForm(request.POST or None, request.FILES or None)
    
    if request.method == 'POST':
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            try:
                article.full_clean()  # ตรวจสอบ unique ก่อน
                article.save()
                return redirect('my-articles')
            except ValidationError as e:
                form.add_error('title', 'ชื่อนี้ถูกใช้ไปแล้ว กรุณาใช้ชื่ออื่น')
            except IntegrityError:
                form.add_error('title', 'ชื่อนี้ถูกใช้ไปแล้ว กรุณาใช้ชื่ออื่น')

    return render(request, 'writer/create-article.html', {'CreateArticleForm': form})


@login_required(login_url='my-login')
def my_articles(request):
    articles = Article.objects.filter(user=request.user)
    return render(request, 'writer/my-articles.html', {'AllArticles': articles})


@login_required(login_url='my-login')
def update_article(request, pk):
    article = get_object_or_404(Article, id=pk, user=request.user)
    form = ArticleForm(request.POST or None, request.FILES or None, instance=article)

    if request.method == 'POST':
        if form.is_valid():
            try:
                form.instance.full_clean()  # ตรวจสอบ unique ก่อน
                form.save()
                return redirect('my-articles')
            except ValidationError:
                form.add_error('title', 'ชื่อนี้ถูกใช้ไปแล้ว กรุณาใช้ชื่ออื่น')
            except IntegrityError:
                form.add_error('title', 'ชื่อนี้ถูกใช้ไปแล้ว กรุณาใช้ชื่ออื่น')

    return render(request, 'writer/update-article.html', {'UpdateArticleForm': form})

@login_required(login_url='my-login')
def delete_article(request, pk):
    article = get_object_or_404(Article, id=pk, user=request.user)
    if request.method == 'POST':
        article.delete()
        return redirect('my-articles')
    return render(request, 'writer/delete-article.html')


@login_required(login_url='my-login')
def account_management(request):
    form = UpdateUserForm(request.POST or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('writer-dashboard')
    return render(request, 'writer/account-management.html', {'UpdateUserForm': form})


@login_required(login_url='my-login')
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('my-login')
    return render(request, 'writer/delete-account.html')


@login_required(login_url='my-login')
def article_detail(request, pk):
    article = get_object_or_404(Article, id=pk, user=request.user)
    return render(request, 'writer/article-detail.html', {'article': article})
