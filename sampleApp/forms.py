from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ClearableFileInput

from .models import UserProfile, Post, PostAttachment


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


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']


class CreatePostAttachmentForm(forms.ModelForm):
    class Meta:
        model = PostAttachment
        fields = ['attachment']
        widgets = {
            'attachment': ClearableFileInput(attrs={'multiple': True})
        }

# https://stackoverflow.com/questions/38257231/how-can-i-upload-multiple-files-to-a-model-field
