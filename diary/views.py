# diary/views.py

import matplotlib

matplotlib.use('Agg')  # Устанавливаем неинтерактивный бэкенд

import matplotlib.pyplot as plt
from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, Grade, Comment, Subject
from .forms import GradeForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Avg
import io
import base64


@login_required
def home(request):
    students = Student.objects.all()
    return render(request, 'diary/home.html', {'students': students})


@login_required
def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    grades = student.grades.all()
    comments = student.comments.all()
    average_grade = grades.aggregate(Avg('grade'))['grade__avg']

    # Визуализация прогресса
    subjects = Subject.objects.all()
    grades_per_subject = []
    for subject in subjects:
        avg = grades.filter(subject=subject).aggregate(Avg('grade'))['grade__avg']
        grades_per_subject.append(avg if avg else 0)

    plt.figure(figsize=(10, 5))
    plt.bar([subject.name for subject in subjects], grades_per_subject, color='skyblue')
    plt.xlabel('Предметы')
    plt.ylabel('Средняя оценка')
    plt.title('Прогресс ученика')
    plt.ylim(0, 5)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()

    context = {
        'student': student,
        'grades': grades,
        'comments': comments,
        'average_grade': average_grade,
        'chart': image_base64,
    }
    return render(request, 'diary/student_detail.html', context)


@login_required
def add_grade(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.student = student
            grade.teacher = request.user
            grade.save()
            messages.success(request, 'Оценка успешно добавлена.')
            return redirect('student_detail', student_id=student.id)
    else:
        form = GradeForm()
    return render(request, 'diary/add_grade.html', {'form': form, 'student': student})


@login_required
def add_comment(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.student = student
            comment.teacher = request.user
            comment.save()
            messages.success(request, 'Комментарий успешно добавлен.')
            return redirect('student_detail', student_id=student.id)
    else:
        form = CommentForm()
    return render(request, 'diary/add_comment.html', {'form': form, 'student': student})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно.')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
