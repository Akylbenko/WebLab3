from django.forms import ModelForm, TextInput, Textarea, DateInput, Select, Form, PasswordInput
from .models import Feedbacks, Article, Comment, User


class FeedbacksForm(ModelForm):
    class Meta:
        model = Feedbacks
        fields = ['name', 'email','content']
        widgets = {
            "name": TextInput(attrs={'class':'form-control', 'placeholder':'Имя'}),
            "email": TextInput(attrs={'class':'form-control', 'placeholder':'Почта'}),
            "content": Textarea(attrs={'class':'form-control', 'placeholder':'Комментарий'}),
        }

class ArticlesForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'text', 'created_date', 'category','user_id']
        widgets = {
            "title": TextInput(attrs={'class':'form-control', 'placeholder':'Заголовок'}),
            "text": Textarea(attrs={'class':'form-control', 'placeholder':'Текст'}),
            "created_date": DateInput(attrs={'class':'form-control', 'placeholder':'Дата создания'}),
            "category": Select(attrs={'class':'form-control', 'placeholder':'Категория'}),
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['author_name', 'text']
        widgets = {
            "author_name": TextInput(attrs={'class':'form-control', 'placeholder':'Автор'}),
            "text": Textarea(attrs={'class':'form-control', 'placeholder':'Комментарий'}),
        }

class LoginForm(Form):
    class Meta:
        model = User
        fields = ['username', 'email','password']
        widgets = {
            "username": TextInput(attrs={'class':'form-control', 'placeholder':'Имя пользователя'}),
            "email": TextInput(attrs={'class':'form-control', 'placeholder':'Почта'}),
            "password": PasswordInput(attrs={'class':'form-control', 'placeholder':'Пароль'}),
        }