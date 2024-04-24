from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):


    class Status(models.TextChoices):
        DRAFT = 'DF', 'Черновик'
        PUBLISHED = 'PB', 'Опубликовано'


    title = models.CharField(max_length=250, verbose_name='Название')
    slug = models.SlugField(max_length=250, verbose_name='URL-блога', unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', verbose_name='Автор')
    body = models.TextField(verbose_name='Содержимое')
    publish = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT, verbose_name='Статус')

    objects = models.Manager()
    published = PublishedManager()


    class Meta:
        ordering = ['-publish']
        verbose_name_plural = 'Посты'
        verbose_name = 'Пост'

        indexes = [models.Index(fields=['-publish'])]


    def __str__(self):
        return self.title
    

    def  get_absolute_url(self):
        return reverse('blog:post_detail', 
                       args=[self.publish.year, 
                             self.publish.month, 
                             self.publish.day,
                             self.slug])
    

class Comment(models.Model):
    post = models.ForeignKey(Post, 
                             on_delete=models.CASCADE, 
                             related_name='comments',
                             verbose_name='Пост')
    name = models.CharField(max_length=35, verbose_name='Имя')
    email = models.EmailField(verbose_name='Имеил')
    body = models.TextField(verbose_name='Комментарий')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', db_index=True)
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'