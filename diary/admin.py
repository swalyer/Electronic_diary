from django.contrib import admin

# Register your models here.
# diary/admin.py

from django.contrib import admin
from .models import Student, Subject, Grade, Comment

admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Grade)
admin.site.register(Comment)
