"""Данный файл нужен для создания форм на страницах приложения. Пользователь сможет взаимодействовать с объектами,
например добавлять их, через страницы приложения."""

from django import forms
from .models import Post
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    
    class Meta:
        # Саму модель мы должны прописать в Meta классе в поле model
        model = Post
        fields = [
            'author',
            'title',
            'text',
        ]

    def clean(self):

        # Проверка длинны поля description
        cleaned_data = super().clean()  # Наследуем метод (clean) родительского класса
        text = cleaned_data.get('text')  # Получаем через '.get' description
        if text is not None and len(text) < 6:  # Проверяем, чтобы описание не было пустым 
            # менее 20 символов
            raise ValidationError({  # В ином случае вызываем исключение
                "text": "Описание не может быть менее 20 символов."  # В ошибке указываем название поля формы
                # и текст ошибки.
            })
        # Проверка поля name
        name = cleaned_data.get("title")
        if name == text:
            raise ValidationError(
                "Описание не должно быть идентично названию."  
            )

        return cleaned_data

    # Переопределяем метод clean для проверки поля title в form
    def clean_title(self):
        name = self.cleaned_data["title"]
        if name[0].islower():
            raise ValidationError(
                "Название должно начинаться с заглавной буквы"
            )
        return name