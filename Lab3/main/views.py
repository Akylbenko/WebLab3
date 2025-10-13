from django.shortcuts import render
from django.http import HttpResponse
from .forms import FeedbacksForm, ArticlesForm
from .models import Feedbacks


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
    if request.method == "POST":
        form = ArticlesForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ArticlesForm()
        data = {'form': form}

    return render(request, 'main/create_article.html', data)

def news(request, id):
    return HttpResponse(f"Статья {id}")