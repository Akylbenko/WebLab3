from django.db import models
from django.utils import timezone

class Feedbacks(models.Model):
    name = models.CharField('Имя', max_length=50)
    email = models.EmailField('Почта', max_length=50)
    content = models.TextField('Комментарий')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

class User(models.Model):
    name = models.CharField('Имя', max_length=50)
    email = models.EmailField('Почта', max_length=50)
    hashed_password = models.CharField('Пароль', max_length=50)
    created_date = models.DateTimeField('Дата создания', default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Article(models.Model):
    category_choices = [
        ('sports', 'Спорт'),
        ('politics', 'Политика'),
        ('business', 'Бизнес'),
        ('science', 'Наука'),
        ('other', 'Другое'),
    ]

    title = models.CharField('Заголовок', max_length=50)
    text = models.TextField('Текст статьи')
    created_date = models.DateTimeField('Дата создания', default=timezone.now)
    category = models.CharField('Категория', choices=category_choices, default='other', max_length=50)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

class Comment(models.Model):

    text = models.TextField('Текст')
    date = models.DateTimeField('Дата создания', default=timezone.now)
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья')
    author_name = models.CharField('Автор', max_length=50)

    def __str__(self):
        return f"Комментарий от {self.author_name} к статье '{self.article_id.title}'"

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'