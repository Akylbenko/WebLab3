from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from unicodedata import category

from .forms import FeedbacksForm, ArticlesForm, CommentForm
from .models import Feedbacks, User, Article


def home(request):

    return render(request, 'main/home.html')

def about(request):

    return render(request, 'main/about.html')

def contact(request):

    return render(request, 'main/contact.html')

def feedback(request):

    allFeedbacks = Feedbacks.objects.all()

    if request.method == "POST":
        form = FeedbacksForm(request.POST)
        if form.is_valid():
            form.save()
            allFeedbacks = Feedbacks.objects.all()
            form = FeedbacksForm()
            data = {'form': FeedbacksForm(), 'Feedbacks': allFeedbacks}
        else:
            error = 'Ошибка, неверно введена почта!'
            data = {'form': form, 'error': error, 'Feedbacks': allFeedbacks}

    else:
        form = FeedbacksForm()
        data = {'form': form, 'Feedbacks': allFeedbacks}

    return render(request, 'main/feedback.html', data)

def articles(request, category=None):

    all_categories = dict(Article.category_choices)
    if category:
        if category not in all_categories:
            raise Http404("Категория не найдена")

        articles_list = Article.objects.filter(category=category).order_by('-created_date')
        current_category = all_categories[category]
    else:
        articles_list = Article.objects.all().order_by('-created_date')
        current_category = "Все новости"

    data = {
        'articles': articles_list,
        'categories': Article.category_choices,
        'current_category': current_category,
        'selected_category': category,
    }

    return render(request, 'main/articles.html', data)

def article_comment(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    comments = article.comment_set.all().order_by('-date')

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article_id = article
            comment.save()
            return redirect('article_comment', article_id=article_id)
    else:
        form = CommentForm()

    data = {'article': article, 'form': form, 'comments': comments}
    return render(request, 'main/article_comment.html', data)

def create_article(request):

    if not User.objects.exists():
        User.objects.create(name='Default user', email='default@gmail.com', hashed_password='temp')
    if request.method == "POST":
        form = ArticlesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ArticlesForm()

    data = {'form': form}
    return render(request, 'main/create_article.html', data)

def edit_article(request, id):
    article = get_object_or_404(Article, id=id)

    if request.method == "POST":
        form = ArticlesForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles')
    else:
        form = ArticlesForm(instance=article)

        return render(request, 'main/edit_article.html', {'form': form, 'article': article})

def delete_article(request, id):
    article = get_object_or_404(Article, id=id)

    if request.method == "POST":
        article.delete()
        return redirect('articles')

    return render(request, 'main/delete_article.html', {'article': article})

def login_view(request):

    # if request.method == "POST":


    return render(request, 'main/login.html')

def news(request, id):
    return HttpResponse(f"Статья {id}")

