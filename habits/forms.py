from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Habit, Mood


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('That email is already registered!')


class HabitModelForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'description', 'frequency']

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g. Do exercise'}),
            'frequency': forms.Select(attrs={'class': 'my_select'}),
            'description': forms.Textarea(attrs={
                'rows':3,
                'placeholder': 'Optional description...'
            })
        }

        labels = {
            'name': 'Name your habit',
            'frequency': 'Your habit frequency',
            'description': 'Add description (optional)'
        }

        error_messages = {
            'name': {
                'required': 'Please give your habit a name!'
            },
            'frequency': {
                'required': 'Please add frequency to your habit'
            }
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 3:
            raise forms.ValidationError('Name must be at least 3 characters!')
        return name.strip().capitalize()


class MoodForm(forms.ModelForm):
    class Meta:
        model = Mood
        fields = ['mood', 'note']
        widgets = {
            'mood': forms.Select(attrs={'class': 'my_select'}),
            'note': forms.Textarea(attrs={
                'rows':3,
                'placeholder': 'How are you feeling? (optional)'
            })
        }
        labels = {
            'mood': 'How are you feeling today?',
            'note': 'Add a note (optional)'
        }