from django import forms
from .models import User
from django.utils import timezone
from tempus_dominus.widgets import DateTimePicker
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
        empty_label="SELECT",
        widget=forms.Select(attrs={'class': 'form-control py-2'})
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control py-2', 'rows': '3'}),
    )

    class Meta:
        model = Order
        fields = ['service', 'description']


class OrderTaskForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.all(),
        empty_label="SELECT",
        widget=forms.Select(attrs={'class': 'form-control py-2'})
    )
    schedule_on = forms.DateTimeField(
        widget=DateTimePicker(),
        required=False
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control py-2', 'rows': '3'}),
        required=False
    )

    class Meta:
        model = OrderTask
        fields = ['assigned_to', 'schedule_on', 'schedule_end', 'message', 'description']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(OrderTaskForm, self).__init__(*args, **kwargs)
        if user.user_type == User.AGENT:
            self.fields['assigned_to'].queryset = User.objects.filter(user_type=User.EVALUATOR)
        else:
            self.fields['assigned_to'].queryset = User.objects.all()


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
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.all(),
        empty_label="SELECT",
        widget=forms.Select(attrs={'class': 'form-control py-2'})
    )
    dust_level = forms.ModelChoiceField(
        queryset=DustLevelPrice.objects.all(),
        empty_label="SELECT",
        widget=forms.Select(
            attrs={'class': 'form-control py-2'}
        )
    )
    dust_level = forms.ModelChoiceField(
        queryset=DustLevelPrice.objects.all(),
        empty_label="SELECT",
        widget=forms.Select(
            attrs={'class': 'form-control py-2'}
        )
    )
    team_members = forms.IntegerField(
        widget=forms.TextInput(
            attrs={'class': 'form-control py-2'}
        )
    )
    expected_time = forms.FloatField(
        widget=forms.TextInput(
            attrs={'class': 'form-control py-2'}
        )
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.pk = kwargs.pop('pk', None)
        self.task_id = kwargs.pop('task_id', None)
        super(EvaluationForm, self).__init__(*args, **kwargs)
        if self.user.user_type == User.EVALUATOR:
            self.fields['assigned_to'].queryset = User.objects.filter(user_type=User.STL)
        else:
            self.fields['assigned_to'].queryset = User.objects.all()

    class Meta:
        model = Evaluation
        fields = ['dust_level', 'team_members', 'expected_time']

    def save(self, commit=True):
        instance = super(EvaluationForm, self).save(commit=False)
        dust_level = self.cleaned_data['dust_level']
        no_of_team_members = self.cleaned_data['team_members']
        dust_level_price = DustLevelPrice.objects.get(dust_level=dust_level)
        estimated_price = dust_level_price.price * no_of_team_members
        instance.order_id = self.pk
        instance.order_task_id = self.task_id
        instance.estimated_price = estimated_price
        assigned_to = self.cleaned_data['assigned_to']
        print(assigned_to)
        order_task = OrderTask.objects.create(
            order_id=self.pk,
            created_by=self.user,
            assigned_to=assigned_to,
            process=OrderTask.OPEN,
            schedule_end=timezone.now()
        )
        return super(EvaluationForm, self).save(commit=commit)
