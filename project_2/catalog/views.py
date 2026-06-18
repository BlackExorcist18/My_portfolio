from django.shortcuts import render
from django.http import Http404
from .data import COURSES, AUTHORS


def index(request):
    """Главная страница"""
    return render(request, 'index.html')


def courses(request):
    """Страница со списком всех курсов"""
    courses_list = []
    for course in COURSES:
        author = next((a for a in AUTHORS if a['id'] == course['author_id']), None)
        course_copy = course.copy()
        course_copy['author_name'] = author['name'] if author else 'Неизвестный автор'
        courses_list.append(course_copy)
    
    context = {
        'courses': courses_list,
    }
    return render(request, 'courses.html', context)


def course_detail(request, course_id):
    """Страница конкретного курса"""
    # Добавим отладочную информацию
    print(f"Looking for course with id: {course_id}")
    print(f"Available courses: {[c['id'] for c in COURSES]}")
    
    # Ищем курс по id
    course = next((c for c in COURSES if c['id'] == course_id), None)
    
    if course is None:
        print(f"Course with id {course_id} not found")
        raise Http404("Курс не найден")
    
    # Находим автора курса
    author = next((a for a in AUTHORS if a['id'] == course['author_id']), None)
    
    # Добавляем данные для шаблона
    course_data = course.copy()
    course_data['author_name'] = author['name'] if author else 'Неизвестный автор'
    course_data['author_id'] = author['id'] if author else 0
    
    context = {
        'course': course_data,
    }
    return render(request, 'course_detail.html', context)


def authors(request):
    """Страница со списком всех авторов"""
    authors_list = []
    for author in AUTHORS:
        author_copy = author.copy()
        courses_count = sum(1 for c in COURSES if c['author_id'] == author['id'])
        author_copy['courses_count'] = courses_count
        authors_list.append(author_copy)
    
    context = {
        'authors': authors_list,
    }
    return render(request, 'authors.html', context)


def author_detail(request, author_id):
    """Страница конкретного автора"""
  
    print(f"Looking for author with id: {author_id}")
    print(f"Available authors: {[a['id'] for a in AUTHORS]}")
    
    # Ищем автора по id
    author = next((a for a in AUTHORS if a['id'] == author_id), None)
    
    if author is None:
        print(f"Author with id {author_id} not found")
        raise Http404("Автор не найден")
    
    # Находим все курсы автора
    author_courses = [c for c in COURSES if c['author_id'] == author_id]
    
    author_data = author.copy()
    author_data['courses'] = author_courses
    
    context = {
        'author': author_data,
    }
    return render(request, 'author_detail.html', context)


def info(request):
    """Информационная страница"""
    return render(request, 'info.html')


def custom_404(request, exception):
    """Кастомная страница 404"""
    return render(request, 'not_found.html', status=404)