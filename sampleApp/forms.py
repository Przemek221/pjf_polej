from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class RegisterUserForm(UserCreationForm):
    password2 = None  # thanks to this, there is only one passwd field in the form

    class Meta:
        model = User
        fields = ['username', 'password1']


class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']
        # fields = ['username']


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']
