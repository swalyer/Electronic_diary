# diary/forms.py

from django import forms
from .models import Grade, Comment

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['subject', 'grade']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
