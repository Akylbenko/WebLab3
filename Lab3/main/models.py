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
    title = models.CharField('Заголовок', max_length=50)
    text = models.TextField('Текст статьи')
    created_date = models.DateTimeField('Дата создания', default=timezone.now)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'