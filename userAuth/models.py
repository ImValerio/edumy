from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django import forms


class UserCreation(UserCreationForm):
    username = forms.CharField()
    first_name = forms.CharField(max_length=32, help_text='First name')
    last_name = forms.CharField(max_length=32, help_text='Last name')
    email = forms.EmailField(max_length=64,
                             help_text='Enter a valid email address')
    password1 = forms.CharField()
    password2 = forms.CharField()

    class Meta(UserCreationForm.Meta):
        model = User
        # I've tried both of these 'fields' declaration, result is the same
        # fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',)
