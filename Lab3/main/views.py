from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib import messages
from .forms import FeedbacksForm, ArticlesForm, CommentForm, LoginForm, RegistrationForm
from .models import Feedbacks, User, Article
import hashlib


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
    if 'user_id' not in request.session:
        messages.error(request, 'Для создания статьи необходимо авторизоваться')
        return redirect('login_view')

    if request.method == "POST":
        form = ArticlesForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            user_id = request.session.get('user_id')
            article.user_id = User.objects.get(id=user_id)
            article.save()
            messages.success(request, 'Статья успешно создана!')
            return redirect('articles')
    else:
        form = ArticlesForm()

    data = {'form': form}
    return render(request, 'main/create_article.html', data)


def edit_article(request, id):
    if 'user_id' not in request.session:
        messages.error(request, 'Для редактирования статьи необходимо авторизоваться')
        return redirect('login_view')

    article = get_object_or_404(Article, id=id)

    user_id = request.session.get('user_id')
    if article.user_id.id != user_id:
        messages.error(request, 'Вы можете редактировать только свои статьи')
        return redirect('articles')

    if request.method == "POST":
        form = ArticlesForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Статья успешно отредактирована!')
            return redirect('articles')
    else:
        form = ArticlesForm(instance=article)

    return render(request, 'main/edit_article.html', {'form': form, 'article': article})


def delete_article(request, id):
    if 'user_id' not in request.session:
        messages.error(request, 'Для удаления статьи необходимо авторизоваться')
        return redirect('login_view')

    article = get_object_or_404(Article, id=id)

    user_id = request.session.get('user_id')
    if article.user_id.id != user_id:
        messages.error(request, 'Вы можете удалять только свои статьи')
        return redirect('articles')

    if request.method == "POST":
        article.delete()
        messages.success(request, 'Статья успешно удалена!')
        return redirect('articles')

    return render(request, 'main/delete_article.html', {'article': article})


def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Пользователь с таким email уже существует')
            else:
                hashed_password = hashlib.md5(password.encode()).hexdigest()

                user = User.objects.create(
                    name=username,
                    email=email,
                    hashed_password=hashed_password
                )
                messages.success(request, 'Регистрация прошла успешно!')
                return redirect('login_view')
    else:
        form = RegistrationForm()

    return render(request, 'main/register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            hashed_password = hashlib.md5(password.encode()).hexdigest()

            try:
                user = User.objects.get(email=email, hashed_password=hashed_password)
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                messages.success(request, f'Добро пожаловать, {user.name}!')
                return redirect('home')
            except User.DoesNotExist:
                messages.error(request, 'Неверный email или пароль')
    else:
        form = LoginForm()

    return render(request, 'main/login.html', {'form': form})


def logout_view(request):
    request.session.flush()
    messages.success(request, 'Вы успешно вышли из системы')
    return redirect('home')


def news(request, id):
    return HttpResponse(f"Статья {id}")