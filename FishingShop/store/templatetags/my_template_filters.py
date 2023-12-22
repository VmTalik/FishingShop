# from django.template.defaulttags import register
from django import template

register = template.Library()


@register.filter
def get_dict_value(dictionary, key):
    return dictionary.get(key)


@register.filter
def rus_plural(value, variants):
    """Функция, позволяющая склонять русское слово в зависимости от количества.
    Например, "1 отзыв", "2 отзыва", "7 отзывов"
    """
    variants = variants.split(',')
    if value % 10 == 1 and value % 100 != 11:
        variant = 0
    elif 2 <= value % 10 <= 4 and value % 100 < 10 or value % 100 >= 20:
        variant = 1
    else:
        variant = 2
    return variants[variant]


