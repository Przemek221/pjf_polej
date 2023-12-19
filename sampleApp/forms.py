from django import forms


class addUserForm(forms.Form):
    # your_name = forms.CharField(label="Your name", max_length=100)
    nickname = forms.CharField(label="Nickname", max_length=30)
    password = forms.CharField(label="Password", max_length=30)
