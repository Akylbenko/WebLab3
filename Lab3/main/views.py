from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import FeedbacksForm, ArticlesForm
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
            return redirect('home')
        else:
            form = ArticlesForm(instance=article)

        return render(request, 'main/edit_article.html', {'form': form, 'article': article})

def delete_article(request, id):
    article = get_object_or_404(Article, id=id)

    if request.method == "POST":
        article.delete()
        return redirect('home')

    return render(request, 'main/delete_article.html', {'article': article})

def news(request, id):
    return HttpResponse(f"Статья {id}")