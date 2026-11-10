from django import forms

from app.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task']
        widgets = {
            'task': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'What needs to be done?',
                'autocomplete': 'off',
            }),
        }
