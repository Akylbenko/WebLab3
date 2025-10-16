from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('feedback/', views.feedback, name='feedback'),
    path('articles/', views.articles, name='articles'),
    path('login/', views.login_view, name='login'),
    path('create-article/', views.create_article, name='create_article'),
    path('delete-article/<int:id>/', views.delete_article, name='delete_article'),
    path('edit-article/<int:id>/', views.edit_article, name='edit_article'),
    path('articles/<int:article_id>/', views.article_comment, name='article_comment'),
    path('articles/<str:category>/', views.articles, name='articles_by_category'),
]