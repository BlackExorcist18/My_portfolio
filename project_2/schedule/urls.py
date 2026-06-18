from django.urls import path
from . import views

app_name = 'schedule'

urlpatterns = [
    # Teacher CRUD
    path('teachers/', views.teacher_index, name='teacher_index'),
    path('teachers/<int:pk>/', views.teacher_detail, name='teacher_detail'),
    path('teachers/create/', views.teacher_create_lr5, name='teacher_create'),
    path('teachers/<int:pk>/update/', views.teacher_update, name='teacher_update'),
    path('teachers/<int:pk>/delete/', views.teacher_delete, name='teacher_delete'),
    
    # Course CRUD
    path('courses/', views.course_index, name='course_index'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
    path('courses/create/', views.course_create_lr5, name='course_create'),
    path('courses/<int:pk>/update/', views.course_update, name='course_update'),
    path('courses/<int:pk>/delete/', views.course_delete, name='course_delete'),
    
    # Student CRUD
    path('students/', views.student_index, name='student_index'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/create/', views.student_create_lr5, name='student_create'),
    path('students/<int:pk>/update/', views.student_update, name='student_update'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),
    
    # Enroll/Unenroll
    path('students/<int:student_id>/enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('students/<int:student_id>/unenroll/<int:course_id>/', views.unenroll_course, name='unenroll_course'),
    
    # ORM Query pages
    path('queries/', views.queries_index, name='queries_index'),

    path('teachers/create/lr5/', views.teacher_create_lr5, name='teacher_create_lr5'),
    path('courses/create/lr5/', views.course_create_lr5, name='course_create_lr5'),
    path('students/create/lr5/', views.student_create_lr5, name='student_create_lr5'),
]