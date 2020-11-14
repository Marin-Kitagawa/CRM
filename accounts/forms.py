from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
        exclude = [
            'user'
        ]


class ActivityForm(ModelForm):
    class Meta:
        model = Activity
        fields = '__all__'  # That is create a form with all the fields in the Order class of models.py


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]
