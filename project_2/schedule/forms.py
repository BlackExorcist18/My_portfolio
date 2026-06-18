from django import forms
from .models import Teacher, TeacherInfo, Course, Student


class TeacherForm(forms.Form):
    """Форма для добавления преподавателя (ЛР3)"""
    first_name = forms.CharField(
        max_length=100,
        label="Имя",
        help_text="Введите имя преподавателя",
        widget=forms.TextInput(attrs={'placeholder': 'Например: Иван'})
    )
    last_name = forms.CharField(
        max_length=100,
        label="Фамилия",
        help_text="Введите фамилию преподавателя",
        widget=forms.TextInput(attrs={'placeholder': 'Например: Петров'})
    )
    email = forms.EmailField(
        label="Email",
        help_text="Введите email преподавателя",
        widget=forms.EmailInput(attrs={'placeholder': 'ivan@example.com'})
    )
    level = forms.ChoiceField(
        choices=Teacher.LEVEL_CHOICES,
        label="Уровень",
        help_text="Выберите уровень преподавателя"
    )
    is_active = forms.BooleanField(
        required=False,
        label="Активен",
        help_text="Отметьте, если преподаватель активен"
    )
    biography = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Расскажите о преподавателе...'}),
        label="Биография",
        help_text="Краткая биография (необязательно)"
    )
    education = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'МГУ, ВШЭ...'}),
        label="Образование",
        help_text="Образование преподавателя (необязательно)"
    )
    experience_years = forms.IntegerField(
        required=False,
        min_value=0,
        label="Опыт (лет)",
        help_text="Количество лет опыта (необязательно)"
    )