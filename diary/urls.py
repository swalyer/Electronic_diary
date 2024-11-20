# diary/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('student/<int:student_id>/', views.student_detail, name='student_detail'),
    path('student/<int:student_id>/add_grade/', views.add_grade, name='add_grade'),
    path('student/<int:student_id>/add_comment/', views.add_comment, name='add_comment'),
    path('register/', views.register, name='register'),
]
