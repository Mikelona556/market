# from dataclasses import field
from django import forms
from django.forms import ModelForm
from . models import *

class CartForm(forms.ModelForm):
    class meta:
        model = Cart
        fields = ['quantity']