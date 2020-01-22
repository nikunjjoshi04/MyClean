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
    username = forms.CharField(label='User Name', widget=forms.TextInput(attrs={'class': 'form-control py-2'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control py-2'}))


class SearchForm(forms.Form):
    pass


class OrderForm(forms.ModelForm):
    service = forms.ModelChoiceField(
        queryset=Services.objects.all(),
        empty_label='SELECT SERVICE',
        widget=forms.Select(attrs={'class': 'form-control py-2'})
    )

    class Meta:
        model = Order
        fields = ['service']


class OrderTaskForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.filter(user_type='evaluator'),
        empty_label="SELECT EVALUATOR",
        widget=forms.Select(attrs={'class': 'form-control py-2'})
    )

    class Meta:
        model = OrderTask
        fields = ['assigned_to']


class CustomerForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-2'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-2'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control py-2'}))
    mobile_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-2'}))

    class Meta:
        model = Customer
        fields = '__all__'


class AddressForm(forms.ModelForm):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control py-2'})
    )
    street = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-2'}))
    building = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-2'}))

    class Meta:
        model = Address
        fields = ['city', 'street', 'building']


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['dust_level', 'no_of_team_members', 'expected_time', 'estimated_price']
