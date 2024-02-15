from django import forms
from apps.voyage.models  import Course, Assignment

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields ="__all__"

        widgets = {
            'program': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Select(attrs={'class': 'form-control'}),
            'due': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'instructions': forms.Textarea(attrs={ 'class': 'form-control','rows': 2}),
            'rubric': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }