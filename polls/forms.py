from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class UserSignUp(UserCreationForm):
    password2=forms.CharField(label='Password (Again)', widget=forms.PasswordInput())
    password1=forms.CharField(label='Set Password', widget=forms.PasswordInput())
    class Meta:
        model=User
        fields=['username','email']
        labels={'email':'Email', 'username':'Set Username'}
