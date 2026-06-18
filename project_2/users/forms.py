from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации с дополнительными полями"""
    phone = forms.CharField(max_length=20, required=False, label="Телефон")
    birth_date = forms.DateField(required=False, label="Дата рождения", 
                                  widget=forms.DateInput(attrs={'type': 'date'}))
    bio = forms.CharField(widget=forms.Textarea, required=False, label="О себе")
    
    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'birth_date', 'bio', 'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):
    """Форма редактирования профиля"""
    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'birth_date', 'bio', 'avatar')