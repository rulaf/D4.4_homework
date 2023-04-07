from django.shortcuts import render
from datetime import datetime
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Post
from .filters import PostFilter
from .forms import PostForm


# Класс-представление для отображения списка постов. Унаследован от базового представления"ListView"
class PostList(ListView):
    model = Post  
    template_name = 'flatpages/news.html'  
    context_object_name = 'news'  
    queryset = Post.objects.order_by('-id')
    paginate_by = 3  # Задаем кол-во отображаемых объектов на странице


    # Переопределяем функцию получения списка 
    def get_queryset(self):
        queryset = super().get_queryset() 
        self.filterset = PostFilter(self.request.GET, queryset)  
        return self.filterset.qs 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = 'Выберите статью по категории!'
        context['filterset'] = self.filterset  # Добавляем в контекст объект фильтрации
        return context


# Класс-представление, созданное для поиска объектов по фильтрам
class PostDetail(DetailView):
    model = Post
    template_name = 'flatpages/post.html'
    context_object_name = 'post'


class PostSearch(PostList):
    model = Post
    template_name = 'flatpages/search.html'
    context_object_name = 'posts_search'
    filter_class = PostFilter
    ordering = ['dateCreation']

    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['filter'] = PostFilter(
            self.request.GET, queryset=self.get_queryset())  # Вписываем фильтр в контекст
        return context


class PostCreate(CreateView):
    form_class = PostForm 
    model = Post 
    template_name = 'flatpages/post_create.html' 

    def form_valid(self, form): 
        post = form.save(commit=False)
        post.categoryType = 'AR'

        return super().form_valid(form)


# CreateView представление для создания публикации.
class NewsCreate(CreateView):
    form_class = PostForm 
    model = Post
    template_name = 'flatpages/news_create.html'
    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'NW'

        return super().form_valid(form)


# UpdateView представление для редактирования публикации.
class PostUpdate(UpdateView):
    form_class = PostForm 
    template_name = 'flatpages/post_edit.html'
    model = Post

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class NewsUpdate(UpdateView):
    form_class = PostForm 
    template_name = 'flatpages/news_edit.html'
    model = Post

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# DeleteView представление для удаления публикации.
class PostDelete(DeleteView):
    template_name = 'flatpages/post_delete.html'
    success_url = '/post/'

    def get_object(self, **kwargs): 
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class NewsDelete(DeleteView):
    template_name = 'flatpages/news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
