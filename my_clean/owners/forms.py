from django import forms
from .models import User
from django.contrib.auth import authenticate, login
from customer.models import Customer, Address, \
    City, State
from order.models import Order, \
    OrderTask, Evaluation, \
    Team, Services, \
    DustLevelPrice


class LoginForm(forms.Form):
    username = forms.CharField(label='User Name')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())


class SearchForm(forms.Form):
    pass
