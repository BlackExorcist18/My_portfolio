from django.db import models
from django.urls import reverse

# Create your models here.

class TeacherInfo(models.Model):
    """Дополнительная информация о преподавателе (связь 1:1 с Teacher)"""
    biography = models.TextField(verbose_name="Биография", blank=True)
    education = models.CharField(max_length=500, verbose_name="Образование", blank=True)
    experience_years = models.PositiveIntegerField(verbose_name="Лет опыта", default=0)
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True, null=True)
    address = models.CharField(max_length=200, verbose_name="Адрес", blank=True, null=True)
    birth_date = models.DateField(verbose_name="Дата рождения", blank=True, null=True)
    
    class Meta:
        verbose_name = "Информация о преподавателе"
        verbose_name_plural = "Информация о преподавателях"
    
    def __str__(self):
        return f"Информация о преподавателе (ID: {self.id})"


class Teacher(models.Model):
    """Модель преподавателя (связь 1:1 с TeacherInfo, 1:N с Course)"""
    LEVEL_CHOICES = [
        ('junior', 'Junior'),
        ('middle', 'Middle'),
        ('senior', 'Senior'),
        ('lead', 'Lead'),
    ]
    
    first_name = models.CharField(max_length=100, verbose_name="Имя", db_index=True)
    last_name = models.CharField(max_length=100, verbose_name="Фамилия", db_index=True)
    email = models.EmailField(verbose_name="Email", unique=True)  # уникальное поле
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, verbose_name="Уровень", default='middle')
    hire_date = models.DateField(verbose_name="Дата найма", auto_now_add=True)
    is_active = models.BooleanField(verbose_name="Активен", default=True)
    
    # Связь 1:1 с TeacherInfo (on_delete=CASCADE - при удалении Teacher удаляется и TeacherInfo)
    info = models.OneToOneField(
        TeacherInfo, 
        on_delete=models.CASCADE,
        verbose_name="Информация",
        null=True,
        blank=True
    )
    rating = models.DecimalField(
        max_digits=3, decimal_places=2, 
        default=0, null=True, blank=True,
        verbose_name="Рейтинг",
        help_text="Рейтинг от 0 до 5"
    )
    hire_date = models.DateField(
        verbose_name="Дата найма",
        auto_now_add=True  # уже должно быть
    )

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.get_level_display()})"
    
    def get_absolute_url(self):
        return reverse('teacher_detail', args=[str(self.id)])
    
    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name}"


class Course(models.Model):
    """Модель курса (связь 1:N с Teacher, N:N с Student)"""
    LEVEL_CHOICES = [
        ('beginner', 'Начальный'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Название курса", unique=True)  # уникальное поле
    description = models.TextField(verbose_name="Описание")
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, verbose_name="Уровень")
    duration_weeks = models.PositiveIntegerField(verbose_name="Длительность (недель)")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена", default=0)
    start_date = models.DateField(verbose_name="Дата старта")
    is_published = models.BooleanField(verbose_name="Опубликован", default=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
    
    # Связь 1:N с Teacher (on_delete=SET_NULL - при удалении учителя курс остается без учителя)
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Преподаватель",
        related_name='courses'
    )
    max_students = models.PositiveIntegerField(
        default=30,
        verbose_name="Максимум студентов",
        help_text="Максимальное количество студентов на курсе"
    )
    language = models.CharField(
        max_length=50, 
        default="Русский",
        verbose_name="Язык преподавания"
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ['-start_date', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"
    
    def get_absolute_url(self):
        return reverse('course_detail', args=[str(self.id)])


class Student(models.Model):
    """Модель студента (связь N:N с Course)"""
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
        ('O', 'Другой'),
    ]
    
    first_name = models.CharField(max_length=100, verbose_name="Имя", db_index=True)
    last_name = models.CharField(max_length=100, verbose_name="Фамилия", db_index=True)
    email = models.EmailField(verbose_name="Email", unique=True)  # уникальное поле
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True)
    birth_date = models.DateField(verbose_name="Дата рождения", null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Пол", blank=True)
    enrollment_date = models.DateField(verbose_name="Дата поступления", auto_now_add=True)
    is_active = models.BooleanField(verbose_name="Активен", default=True)
    
    # Связь N:N с Course
    courses = models.ManyToManyField(
        Course,
        verbose_name="Курсы",
        blank=True,
        related_name='students'
    )
    github = models.URLField(
        blank=True, null=True,
        verbose_name="GitHub",
        help_text="Ссылка на GitHub профиль"
    )
    average_grade = models.DecimalField(
        max_digits=4, decimal_places=2,
        default=0, null=True, blank=True,
        verbose_name="Средний балл"
    )
    
    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.last_name} {self.first_name}"
    
    def get_absolute_url(self):
        return reverse('student_detail', args=[str(self.id)])
    
    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name}"
    
    @property
    def courses_count(self):
        return self.courses.count()