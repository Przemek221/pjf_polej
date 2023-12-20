from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterUserForm(UserCreationForm):
    password2 = None  # thanks to this, there is only one passwd field in the form

    class Meta:
        model = User
        fields = ['username', 'password1']
