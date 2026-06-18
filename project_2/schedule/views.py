from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Count, Q
from django.contrib import messages
from .models import Teacher, TeacherInfo, Course, Student
from .forms import TeacherForm
from .forms_lr5 import (
    TeacherModelForm, TeacherInfoModelForm, 
    CourseModelForm, StudentModelForm
)
# ============ TEACHER CRUD ============

def teacher_index(request):
    """Список всех преподавателей"""
    teachers = Teacher.objects.all()
    return render(request, 'schedule/teacher_index.html', {'teachers': teachers})

def teacher_detail(request, pk):
    """Детальная информация о преподавателе"""
    teacher = get_object_or_404(Teacher, pk=pk)
    return render(request, 'schedule/teacher_detail.html', {'teacher': teacher})

def teacher_create_lr5(request):
    """Создание преподавателя с использованием ModelForm"""
    if request.method == 'POST':
        form = TeacherModelForm(request.POST)
        info_form = TeacherInfoModelForm(request.POST)
        
        if form.is_valid() and info_form.is_valid():
            teacher = form.save(commit=False)
            info = info_form.save()
            teacher.info = info
            teacher.save()
            messages.success(request, f'Преподаватель {teacher.full_name} успешно создан!')
            return redirect('schedule:teacher_detail', pk=teacher.id)
    else:
        form = TeacherModelForm()
        info_form = TeacherInfoModelForm()
    
    return render(request, 'schedule/teacher_form_lr5.html', {
        'form': form,
        'info_form': info_form
    })

def teacher_update(request, pk):
    """Обновление преподавателя"""
    teacher = get_object_or_404(Teacher, pk=pk)
    
    if request.method == 'POST':
        teacher.first_name = request.POST['first_name']
        teacher.last_name = request.POST['last_name']
        teacher.email = request.POST['email']
        teacher.level = request.POST['level']
        teacher.is_active = request.POST.get('is_active', 'on') == 'on'
        teacher.save()
        
        # Обновляем TeacherInfo
        if teacher.info:
            teacher.info.biography = request.POST.get('biography', '')
            teacher.info.education = request.POST.get('education', '')
            teacher.info.experience_years = request.POST.get('experience_years', 0)
            teacher.info.phone = request.POST.get('phone', '')
            teacher.info.address = request.POST.get('address', '')
            teacher.info.birth_date = request.POST.get('birth_date') or None
            teacher.info.save()
        
        messages.success(request, f'Преподаватель {teacher.full_name} успешно обновлен!')
        return redirect('schedule:teacher_detail', pk=teacher.id)
    
    return render(request, 'schedule/teacher_form.html', {'teacher': teacher})

def teacher_delete(request, pk):
    """Удаление преподавателя (CASCADE удалит и TeacherInfo)"""
    teacher = get_object_or_404(Teacher, pk=pk)
    
    if request.method == 'POST':
        name = teacher.full_name
        teacher.delete()
        messages.success(request, f'Преподаватель {name} удален!')
        return redirect('schedule:teacher_index')
    
    return render(request, 'schedule/teacher_confirm_delete.html', {'teacher': teacher})

# ============ COURSE CRUD ============

def course_index(request):
    """Список курсов с фильтрацией по преподавателю"""
    teacher_id = request.GET.get('teacher')
    if teacher_id:
        courses = Course.objects.filter(teacher_id=teacher_id)
    else:
        courses = Course.objects.all()
    
    teachers = Teacher.objects.filter(is_active=True)
    return render(request, 'schedule/course_index.html', {
        'courses': courses,
        'teachers': teachers,
        'selected_teacher': teacher_id
    })

def course_detail(request, pk):
    """Детальная информация о курсе"""
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'schedule/course_detail.html', {'course': course})

def course_create_lr5(request):
    """Создание курса с использованием ModelForm"""
    if request.method == 'POST':
        form = CourseModelForm(request.POST)
        if form.is_valid():
            course = form.save()
            messages.success(request, f'Курс "{course.name}" успешно создан!')
            return redirect('schedule:course_detail', pk=course.id)
    else:
        form = CourseModelForm()
    
    teachers = Teacher.objects.filter(is_active=True)
    return render(request, 'schedule/course_form_lr5.html', {
        'form': form,
        'teachers': teachers
    })

def course_update(request, pk):
    """Обновление курса"""
    course = get_object_or_404(Course, pk=pk)
    
    if request.method == 'POST':
        course.name = request.POST['name']
        course.description = request.POST['description']
        course.level = request.POST['level']
        course.duration_weeks = request.POST['duration_weeks']
        course.price = request.POST['price']
        course.start_date = request.POST['start_date']
        course.teacher_id = request.POST.get('teacher_id') or None
        course.is_published = request.POST.get('is_published', 'on') == 'on'
        course.save()
        
        messages.success(request, f'Курс "{course.name}" успешно обновлен!')
        return redirect('schedule:course_detail', pk=course.id)
    
    teachers = Teacher.objects.filter(is_active=True)
    return render(request, 'schedule/course_form.html', {
        'course': course,
        'teachers': teachers
    })

def course_delete(request, pk):
    """Удаление курса"""
    course = get_object_or_404(Course, pk=pk)
    
    if request.method == 'POST':
        name = course.name
        course.delete()
        messages.success(request, f'Курс "{name}" удален!')
        return redirect('schedule:course_index')
    
    return render(request, 'schedule/course_confirm_delete.html', {'course': course})

# ============ STUDENT CRUD ============

def student_index(request):
    """Список всех студентов"""
    students = Student.objects.all()
    return render(request, 'schedule/student_index.html', {'students': students})

def student_detail(request, pk):
    """Детальная информация о студенте"""
    student = get_object_or_404(Student, pk=pk)
    available_courses = Course.objects.filter(is_published=True).exclude(students=student)
    return render(request, 'schedule/student_detail.html', {
        'student': student,
        'available_courses': available_courses
    })

def student_create_lr5(request):
    """Создание студента с использованием ModelForm"""
    if request.method == 'POST':
        form = StudentModelForm(request.POST)
        if form.is_valid():
            student = form.save()
            
            # Добавление выбранных курсов
            course_ids = request.POST.getlist('courses')
            student.courses.set(course_ids)
            
            messages.success(request, f'Студент {student.full_name} успешно создан!')
            return redirect('schedule:student_detail', pk=student.id)
    else:
        form = StudentModelForm()
    
    courses = Course.objects.filter(is_published=True)
    return render(request, 'schedule/student_form_lr5.html', {
        'form': form,
        'courses': courses
    })

def student_update(request, pk):
    """Обновление студента"""
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        student.first_name = request.POST['first_name']
        student.last_name = request.POST['last_name']
        student.email = request.POST['email']
        student.phone = request.POST.get('phone', '')
        student.birth_date = request.POST.get('birth_date') or None
        student.gender = request.POST.get('gender', '')
        student.is_active = request.POST.get('is_active', 'on') == 'on'
        student.save()
        
        # Обновление курсов
        course_ids = request.POST.getlist('courses')
        student.courses.set(course_ids)
        
        messages.success(request, f'Студент {student.full_name} успешно обновлен!')
        return redirect('schedule:student_detail', pk=student.id)
    
    courses = Course.objects.filter(is_published=True)
    return render(request, 'schedule/student_form.html', {
        'student': student,
        'courses': courses
    })

def student_delete(request, pk):
    """Удаление студента"""
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        name = student.full_name
        student.delete()
        messages.success(request, f'Студент {name} удален!')
        return redirect('schedule:student_index')
    
    return render(request, 'schedule/student_confirm_delete.html', {'student': student})

# ============ ENROLL / UNENROLL ============

def enroll_course(request, student_id, course_id):
    """Запись студента на курс"""
    student = get_object_or_404(Student, pk=student_id)
    course = get_object_or_404(Course, pk=course_id)
    
    if course not in student.courses.all():
        student.courses.add(course)
        messages.success(request, f'{student.full_name} записан на курс "{course.name}"!')
    else:
        messages.warning(request, f'{student.full_name} уже записан на этот курс!')
    
    return redirect('schedule:student_detail', pk=student_id)

def unenroll_course(request, student_id, course_id):
    """Отписка студента от курса"""
    student = get_object_or_404(Student, pk=student_id)
    course = get_object_or_404(Course, pk=course_id)
    
    if course in student.courses.all():
        student.courses.remove(course)
        messages.success(request, f'{student.full_name} отписан от курса "{course.name}"!')
    
    return redirect('schedule:student_detail', pk=student_id)

# ============ ORM QUERIES ============

def queries_index(request):
    """Страница с ORM-запросами"""
    # 1. Все студенты курса (для примера берем первый курс)
    first_course = Course.objects.first()
    students_of_course = first_course.students.all() if first_course else []
    
    # 2. Все преподаватели, у которых больше 1 курса
    teachers_with_many_courses = Teacher.objects.annotate(
        courses_count=Count('courses')
    ).filter(courses_count__gt=1)
    
    # 3. Студенты без курсов
    students_without_courses = Student.objects.annotate(
        courses_count=Count('courses')
    ).filter(courses_count=0)
    
    # 4. Преподаватели без профиля (без TeacherInfo)
    teachers_without_profile = Teacher.objects.filter(info__isnull=True)
    
    context = {
        'students_of_course': students_of_course,
        'teachers_with_many_courses': teachers_with_many_courses,
        'students_without_courses': students_without_courses,
        'teachers_without_profile': teachers_without_profile,
    }
    
    return render(request, 'schedule/queries.html', context)