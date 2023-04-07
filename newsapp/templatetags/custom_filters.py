"""
Файл для создания и регистрации собственных фильтров
"""
from django import template

register = template.Library()  

censor_list = ['современном', 'картины', 'тиран', 'болт', ]  # Список цензуры


@register.filter(name='censor') 

def censor(value):
    if not isinstance(value, str):  # Проверка, что значение (value) является строкой (str),
        raise ValueError('Ценз только строк!')  # в ином случае вызывается исключение

    for word in censor_list:  
        value = value.replace(word[1:], '*' * (len(word)-1))  # то делаем замену (метод replace) этого слова на "*" со
        # второй буквы в слове. Функция len() возвращает длину (количество элементов) в объекте word (минус 1 элемент)
    return value  