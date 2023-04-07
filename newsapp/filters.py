"""Классы, в которых указываем, как можно фильтровать данные моделей."""

from django.forms import DateTimeInput
from django_filters import (
    FilterSet, DateFilter, DateTimeFromToRangeFilter, DateTimeFilter, CharFilter, ModelChoiceFilter,
    ModelMultipleChoiceFilter
)
from django_filters.widgets import (
    DateRangeWidget, RangeWidget
)
from .models import (
    Author, Post, Category
)


class PostFilter(FilterSet):
    searchTitle = CharFilter(
        max_length=128,
        field_name='title',
        lookup_expr='icontains',
        label='Поиск по оглавлению',
    )

    filterAuthor = ModelChoiceFilter(
        field_name='author',
        queryset=Author.objects.all(),
        label='',
        empty_label='Выбор автора'
    )

    
    filterDate = DateTimeFromToRangeFilter(
        field_name='dateCreation',
        lookup_expr='exact',
        label='Поиск по дате',
        widget=RangeWidget(
            attrs={'type': 'datetime-local'}
        )
    )

    
    class Meta:
        model = Post
        fields = {
            'categoryType': ['exact'],
            
        }
