from django import template

register = template.Library()


@register.filter
def is_float(value):
    """Функция проверяет является ли переданное число типом float"""
    if type(value) is float:
        return True
    return False

# Этот файл уже не нужен я переделал вывод из функции в models.
#   Я оставил этот файл если понадобится что-то в нём сделать

