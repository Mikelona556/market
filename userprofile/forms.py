from dataclasses import field, fields
from pyexpat import model
from tkinter.ttk import Widget
from django import forms
from django.contrib.auth.forms import UserCreationForm
from . models import *
# from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

STATE = [
    ('Ondo', 'Ondo'),
    ('Ogun', 'Ogun'),
    ('Kwara', 'Kwara'),
    ('Delta', 'Delta'),
    ('Osun', 'Osun'),
    ('Oyo', 'Oyo'),
    ('Ekiti', 'Ekiti'),
]

GENDER = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Others', 'Others'),
]

class ProfileUpdate(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'state', 'gender', 'nationality', 'pix']
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'first_name'}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'last_name'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email Address'}),
            'phone': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}),
            'address': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Home Address'}),
            'state': forms.Select(attrs={'class':'form-control'}, choices= STATE),
            'gender': forms.Select(attrs={'class':'form-control'}, choices= GENDER),
            'nationality': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nationality'}),
            'pix': forms.FileInput(attrs={'class': 'form-control'})

        }
        
