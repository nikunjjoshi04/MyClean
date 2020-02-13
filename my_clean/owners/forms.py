from dataclasses import fields
from datetime import datetime
from django import forms
from .models import User, TeamMembers, Post, Images
from django.utils import timezone
from tempus_dominus.widgets import DateTimePicker
from django.contrib.auth import authenticate, login
from customer.models import Customer, Address, \
    City, State
from order.models import Order, \
    OrderTask, Evaluation, \
    Team, Services, DustLevelPrice, \
    Accounts


class LoginForm(forms.Form):
    username = forms.CharField(
        label='User Name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control py-2'
            }
        )
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control py-2'
            }
        )
    )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        print('clean')
        username = cleaned_data['username']
        password = cleaned_data['password']

        try:
            user = authenticate(username=username, password=password)
        except Exception as e:
            raise forms.ValidationError(e)
        if user:
            if user.user_type is None or user.user_type == "admin":
                raise forms.ValidationError("Not Valid User")
        return cleaned_data


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
        widget=forms.DateTimeInput(attrs={'class': 'form-control py-2'}),
        required=False
    )
    message = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control py-2'}
        )
    )

    class Meta:
        model = OrderTask
        fields = ['assigned_to', 'schedule_on', 'message']

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

    images = forms.ImageField(required=False)

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control py-2', 'rows': '3'}
        ),
        required=False
    )
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
    team_members = forms.IntegerField(
        widget=forms.TextInput(
            attrs={'class': 'form-control py-2'}
        )
    )
    expected_time = forms.DateTimeField(
        widget=forms.DateTimeInput(
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
        self.fields['images'].widget.attrs.update({"multiple": ''})

    class Meta:
        model = Evaluation
        fields = ['dust_level', 'team_members', 'expected_time', 'assigned_to', 'description']

    # def clean_img(self):
    #     imgs = self.cleaned_data['img']
    #     print(imgs)
    #     return imgs

    def save(self, commit=True):
        instance = super(EvaluationForm, self).save(commit=False)
        dust_level = self.cleaned_data['dust_level']
        no_of_team_members = self.cleaned_data['team_members']
        dust_level_price = DustLevelPrice.objects.get(dust_level=dust_level)
        estimated_price = dust_level_price.price * no_of_team_members
        instance.order_id = self.pk
        instance.accepted = Evaluation.CREATED
        instance.evaluator_order_task_id = self.task_id
        instance.estimated_price = estimated_price
        assigned_to = self.cleaned_data['assigned_to']
        order_task = OrderTask.objects.create(
            order_id=self.pk,
            created_by=self.user,
            assigned_to=assigned_to,
            process=OrderTask.IN_PROCESS,
            # schedule_end=timezone.now()
        )
        instance.stl_order_task = order_task
        instance.save()
        return super(EvaluationForm, self).save(commit=commit)


class EvaluationMediaForm(forms.Form):
    image = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                "class": "custom-file-input"
            }
        ),
        required=False
    )


class STLReviewForm(forms.ModelForm):
    team = forms.ModelMultipleChoiceField(
        queryset=TeamMembers.objects.all(),
        widget=forms.SelectMultiple(
            attrs={'class': 'form-control py-2', 'rows': '3'}
        )
    )
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.all(),
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
    expected_time = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control py-2'
            }
        )
    )
    estimated_price = forms.FloatField(
        widget=forms.TextInput(
            attrs={'class': 'form-control py-2', 'readonly': 'readonly'}
        )
    )
    discount = forms.IntegerField(
        widget=forms.TextInput(
            attrs={'class': 'form-control py-2'}
        )
    )

    class Meta:
        model = Evaluation
        fields = ['team_members', 'expected_time', 'estimated_price', 'discount']

    def clean_team(self):
        team = self.cleaned_data['team']
        team_members = self.cleaned_data['team_members']
        if team.count() < team_members:
            raise forms.ValidationError("The team member is Less then required parsons")
        elif team.count() > team_members:
            raise forms.ValidationError("The team member is More then required parsons")
        return team

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.task_id = kwargs.pop('task_id', None)
        self.order_id = kwargs.pop('order_id', None)
        super(STLReviewForm, self).__init__(*args, **kwargs)
        if self.user.user_type == User.STL:
            self.fields['assigned_to'].queryset = User.objects.filter(user_type=User.TL)
        else:
            self.fields['assigned_to'].queryset = User.objects.all()


class PaymentForm(forms.ModelForm):
    amount = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control py-2'
            }
        ),
        required=False
    )
    check_no = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control py-2',
            }
        ),
        required=False
    )
    check_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control py-2'
            }
        ),
        required=False
    )
    bank_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control py-2'
            }
        ),
        required=False
    )

    class Meta:
        model = Accounts
        fields = ['check_no', 'check_date', 'bank_name', 'amount']

    def __init__(self, *args, **kwargs):
        self.task_id = kwargs.pop('task_id', None)
        super(PaymentForm, self).__init__(*args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        task = OrderTask.objects.get(id=self.task_id)
        price = task.order.order_pk.first().estimated_price
        if amount is None:
            return amount
        elif amount < price:
            raise forms.ValidationError("Amount Is Less Then Actual Price")
        return amount

    def clean_check_no(self):
        check_no = self.cleaned_data['check_no']
        if check_no is None:
            return check_no
        elif len(str(check_no)) > 18:
            raise forms.ValidationError("Enter Valid Check No...")
        return check_no

    def save(self, commit=True):
        task = OrderTask.objects.get(id=self.task_id)
        instance = super(PaymentForm, self).save(commit=False)
        instance.order = task.order
        instance.order_task = task
        task.order.process = Order.ORDER_DONE
        task.process = OrderTask.FINISH
        task.order.save()
        task.save()
        instance.save()
        return super(PaymentForm, self).save(commit=commit)


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=128)
    body = forms.CharField(max_length=245, label="Item Description.")

    class Meta:
        model = Post
        fields = ('title', 'body', )


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')

    class Meta:
        model = Images
        fields = ('image', )
