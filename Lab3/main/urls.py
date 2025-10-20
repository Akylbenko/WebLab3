from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('feedback/', views.feedback, name='feedback'),
    path('articles/', views.articles, name='articles'),
    path('articles/<str:category>/', views.articles, name='articles_by_category'),
    path('article/<int:article_id>/', views.article_comment, name='article_comment'),
    path('create_article/', views.create_article, name='create_article'),
    path('edit_article/<int:id>/', views.edit_article, name='edit_article'),
    path('delete_article/<int:id>/', views.delete_article, name='delete_article'),
    path('register/', views.register_view, name='register_view'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('news/<int:id>/', views.news, name='news'),
]