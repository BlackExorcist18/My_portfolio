from django import forms
from django.core.exceptions import ValidationError
from .models import Teacher, Course, Student, TeacherInfo
from .validators import (
    validate_rating, validate_no_numbers, 
    validate_positive, validate_not_past_date,
    validate_github_url
)



class TeacherModelForm(forms.ModelForm):
    """ModelForm для преподавателя с кастомной валидацией"""
    
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'email', 'level', 'is_active', 'rating']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
    
    # clean_<field> метод (1)
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        validate_no_numbers(first_name)
        return first_name
    
    # clean_<field> метод (2)
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        validate_no_numbers(last_name)
        return last_name
    
    # clean_<field> метод (3)
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        validate_rating(rating)
        return rating
    
    # Метод clean() для формы (1)
    def clean(self):
        cleaned_data = super().clean()
        # Можно добавить кросс-полевые проверки
        return cleaned_data



class TeacherInfoModelForm(forms.ModelForm):
    """ModelForm для дополнительной информации о преподавателе"""
    
    class Meta:
        model = TeacherInfo
        fields = ['biography', 'education', 'experience_years', 'phone', 'address', 'birth_date']
        widgets = {
            'biography': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'education': forms.TextInput(attrs={'class': 'form-control'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
    
    # clean_<field> метод (4)
    def clean_experience_years(self):
        experience = self.cleaned_data.get('experience_years')
        if experience:
            validate_positive(experience)
        return experience
    
    # clean_<field> метод (5)
    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        validate_not_past_date(birth_date)
        return birth_date



class CourseModelForm(forms.ModelForm):
    """ModelForm для курса"""
    
    class Meta:
        model = Course
        fields = ['name', 'description', 'level', 'teacher', 'duration_weeks', 
                  'price', 'start_date', 'is_published', 'max_students', 'language']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'teacher': forms.Select(attrs={'class': 'form-control'}),
            'duration_weeks': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'max_students': forms.NumberInput(attrs={'class': 'form-control'}),
            'language': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    # clean_<field> метод (6)
    def clean_duration_weeks(self):
        duration = self.cleaned_data.get('duration_weeks')
        if duration:
            validate_positive(duration)
            if duration > 52:
                raise ValidationError('Длительность курса не может превышать 52 недели.')
        return duration
    
    # clean_<field> метод (7)
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise ValidationError('Цена не может быть отрицательной.')
        if price and price > 100000:
            raise ValidationError('Цена не может превышать 100 000 ₽.')
        return price
    
    # clean_<field> метод (8)
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            # Проверка на уникальность
            if Course.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
                raise ValidationError('Курс с таким названием уже существует.')
        return name
    
    # Метод clean() для формы (2)
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        duration = cleaned_data.get('duration_weeks')
        
        # Пример кросс-полевой проверки
        if start_date and duration:
            # Можно добавить логику, если нужно
            pass
        
        return cleaned_data


class StudentModelForm(forms.ModelForm):
    """ModelForm для студента"""
    
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'phone', 'birth_date', 
                  'gender', 'is_active', 'github', 'average_grade']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'github': forms.URLInput(attrs={'class': 'form-control'}),
            'average_grade': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
    
    # clean_<field> метод (9)
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        validate_no_numbers(first_name)
        return first_name
    
    # clean_<field> метод (10)
    def clean_github(self):
        github = self.cleaned_data.get('github')
        if github:
            validate_github_url(github)
        return github
    
    # clean_<field> метод (11)
    def clean_average_grade(self):
        grade = self.cleaned_data.get('average_grade')
        if grade is not None:
            if grade < 0 or grade > 5:
                raise ValidationError('Средний балл должен быть от 0 до 5.')
        return grade