from django.contrib import admin
from .models import Teacher, TeacherInfo, Course, Student


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'last_name', 'first_name', 'email', 'level', 'is_active']
    list_filter = ['level', 'is_active', 'hire_date']
    search_fields = ['first_name', 'last_name', 'email']
    # Убираем inlines - это вызывает ошибку


@admin.register(TeacherInfo)
class TeacherInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'experience_years', 'education', 'phone']
    search_fields = ['education', 'phone']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'level', 'teacher', 'price', 'is_published', 'start_date']
    list_filter = ['level', 'is_published', 'start_date', 'teacher']
    search_fields = ['name', 'description']
    filter_horizontal = ['students']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'last_name', 'first_name', 'email', 'is_active', 'courses_count']
    list_filter = ['gender', 'is_active', 'enrollment_date']
    search_fields = ['first_name', 'last_name', 'email']
    filter_horizontal = ['courses']
    
    def courses_count(self, obj):
        return obj.courses.count()
    courses_count.short_description = 'Количество курсов'