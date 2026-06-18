from django.urls import path
from . import views

urlpatterns = [
    # Главная страница
    path('index', views.index, name='index'),
    path('', views.index),
    
    # Список курсов
    path('courses', views.courses, name='courses'),
    
    # Страница конкретного курса - ВАЖНО: формат должен совпадать с ссылками в HTML
    path('course_<int:course_id>', views.course_detail, name='course_detail'),
    
    # Список авторов
    path('authors', views.authors, name='authors'),
    
    # Страница конкретного автора
    path('author_<int:author_id>', views.author_detail, name='author_detail'),
    
    # Информационная страница
    path('info', views.info, name='info'),
]