"""В данном файле создаются и описываются сущности (Модели) баз данных(БД). При помощи ООП, через Классы, описываются их
поля (атрибуты) и методы. Также здесь описываются все связи между сущностями: один ко многим (One to Many) многие ко
многим (Many to Many) один к одному (One to one). После создания моделей, их нужно передать в файл "views.py"""

from django.db import models
from django.contrib.auth.models import User  
from django.db.models import Sum  
from django.urls import reverse


class Author(models.Model):
    autorUsers = models.OneToOneField(User, on_delete=models.CASCADE)  
    ratingAuthor = models.SmallIntegerField(default=0)

    # Внутренний Мета класс, который используется для определения модели.
    class Meta:
        verbose_name = 'Автор'  
        verbose_name_plural = 'Авторы'

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))  
        pRat = 0  
        pRat += postRat.get('postRating') 

        commentRat = self.autorUsers.comment_set.aggregate(commentRating=Sum('rating')) 
        
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat  
        self.save()  

    def __str__(self):
        return f'{self.autorUsers}'  


class Category(models.Model):
    name = models.CharField(max_length=64,unique=True)  

    # Внутренний Мета класс, который используется для определения модели.
    class Meta:
        verbose_name = 'Категория' 
        verbose_name_plural = 'Категории' 

    def __str__(self):
        return f'Категория: {self.name}' 


class Post(models.Model):
    news = 'NW'
    article = 'AR'
    category_choices = [
        (news, 'Новость'),
        (article, 'Статья'),
    ]
    categoryType = models.CharField(
        max_length=2,
        choices=category_choices,
        default=article,
        verbose_name='Вид публикации')  # Выбор из списка "category_choices", по умолчанию - статья
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    postCategory = models.ManyToManyField(Category,through='PostCategory',verbose_name='Категория(category)')
    title = models.CharField(max_length=128,verbose_name='Оглавление')
    text = models.TextField(blank=True,help_text='Текст',verbose_name='Статья')
    rating = models.SmallIntegerField(default=0,verbose_name='Рейтинг')

    
    # Внутренний Мета класс, который используется для определения модели.
    class Meta:
        verbose_name = 'Публикация'  
        verbose_name_plural = 'Публикации'
        ordering = ['categoryType', 'author']

    def __str__(self):
        return f'{self.get_categoryType_display()}: {self.title.title()}. Автор: {self.author}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])  # Возвращаем пользователя на страницу созданной новости.
        

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
        
    def preview(self):
        return f'{self.text[:123]} + {"..."}'


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post,on_delete=models.CASCADE)  
    categoryThrough = models.ForeignKey(Category,on_delete=models.CASCADE)
    # Внутренний Мета класс, который используется для определения модели.
    class Meta:
        verbose_name = 'Категория публикации'
        verbose_name_plural = 'Категории публикаций'

    def __str__(self):
        return f'{self.postThrough}, {self.categoryThrough}'


class Comment(models.Model):
    commentPost = models.ForeignKey(Post,on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User,on_delete=models.CASCADE) 
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    # Внутренний Мета класс, который используется для определения модели.
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.commentUser.username}'

    
    def like(self):
        self.rating += 1 
        self.save()

    
    def dislike(self):
        self.rating -= 1
        self.save()

    def post_com(self):
        return f'Комментарий к статье:\n Дата: {self.dateCreation}\nПользователь: {self.commentUser}\n Рейтинг: {self.rating}\n Коментарий: {self.text}'
