from django.core.exceptions import ValidationError
from django.utils import timezone


# 1. Валидатор для рейтинга (0-5)
def validate_rating(value):
    """Рейтинг должен быть от 0 до 5"""
    if value is not None:
        if value < 0 or value > 5:
            raise ValidationError('Рейтинг должен быть от 0 до 5.')


# 2. Валидатор для имени (без цифр)
def validate_no_numbers(value):
    """Имя/фамилия не должны содержать цифры"""
    if any(char.isdigit() for char in value):
        raise ValidationError('Поле не должно содержать цифры.')


# 3. Валидатор для положительного числа
def validate_positive(value):
    """Значение должно быть положительным"""
    if value is not None and value <= 0:
        raise ValidationError('Значение должно быть больше 0.')


# 4. Дополнительный: проверка даты (не в прошлом)
def validate_not_past_date(value):
    """Дата не должна быть в прошлом"""
    if value and value < timezone.now().date():
        raise ValidationError('Дата не может быть в прошлом.')


# 5. Дополнительный: проверка ссылки GitHub
def validate_github_url(value):
    """Проверка, что ссылка ведёт на GitHub"""
    if value and 'github.com' not in value:
        raise ValidationError('Введите корректную ссылку на GitHub.')