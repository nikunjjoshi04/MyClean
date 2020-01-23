from builtins import super
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView, CreateView
from django.views.generic import TemplateView, DetailView, ListView
from datetime import datetime
from .forms import LoginForm, OrderForm, \
    OrderTaskForm, CustomerForm, \
    AddressForm, EvaluationForm
from django.contrib.auth import logout, login, authenticate
from customer.models import Customer, Address, \
    City, State
from order.models import Order, \
    OrderTask, Evaluation, \
    Team, Services, \
    DustLevelPrice
# Create your views here.


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'owners/login.html'
    success_url = ''

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user:
            login(self.request, user)

        if user.user_type == "agent":
            self.success_url = '/owners/agent_view'
        elif user.user_type == "evaluator":
            self.success_url = '/owners/evaluator_view'
        elif user.user_type == "stl":
            self.success_url = '/owners/stl_view'
        elif user.user_type == "tl":
            self.success_url = '/owners/tl_view'
        return super(LoginView, self).form_valid(form)


class AgentView(FormView):
    order_form = OrderForm
    order_task_form = OrderTaskForm
    form_class = CustomerForm
    address_form = AddressForm
    template_name = 'owners/agent_view.html'
    success_url = '/owners/agent_view'
    o_id = 'MCL'
    o = Order.objects.latest('date')
    o_id = o_id + str(datetime.now().year) + '0' + str(o.id)

    def form_valid(self, form):
        customer_form = form.save()
        address_form = self.address_form(self.request.POST)
        main_order_form = self.order_form(self.request.POST)
        obj_oder_task_form = self.order_task_form(self.request.POST, user=self.request.user)
        if address_form.is_valid():
            address = address_form.save(commit=False)
            address.customer = customer_form
            address.save()
            if main_order_form.is_valid():
                order = main_order_form.save(commit=False)
                order.customer = customer_form
                order.created_by = self.request.user
                order.process = Order.IN_EVALUATION
                order.address = address

                order.save()
                if obj_oder_task_form.is_valid():
                    order_task = obj_oder_task_form.save(commit=False)
                    order_task.order = order
                    order_task.created_by = self.request.user
                    order_task.process = OrderTask.OPEN
                    order_task.save()
        return super(AgentView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AgentView, self).get_context_data()
        context['order'] = self.order_form
        context['order_task'] = self.order_task_form(user=self.request.user)
        context['address'] = self.address_form
        return context


class EvaluatorView(ListView):
    template_name = 'owners/evaluator_view.html'
    model = OrderTask

    def get_context_data(self, **kwargs):
        context = super(EvaluatorView, self).get_context_data()
        context['tasks'] = self.model.objects.filter(assigned_to=self.request.user)
        return context


class EvaluationView(FormView):
    form_class = EvaluationForm
    template_name = 'owners/evaluation_view1.html'
    success_url = '/owners/evaluator_view'
    order_task_form = OrderTaskForm
    pk = 0
    task_id = 0

    def get(self, request, *args, **kwargs):
        order = Order.objects.get(id=self.kwargs['pk'])
        order.process = Order.IN_EVALUATION
        order.save()
        order_task = OrderTask.objects.get(id=self.kwargs['task_id'])
        order_task.process = OrderTask.IN_PROCESS
        order_task.save()
        # self.order_task_form(user=self.request.user)
        return super(EvaluationView, self).get(request, *args, **kwargs)

    def process(self):
        order = Order.objects.get(id=self.kwargs['pk'])
        order.process = Order.EVALUATION_DONE
        order.save()
        order_task = OrderTask.objects.get(id=self.kwargs['task_id'])
        order_task.process = OrderTask.FINISH
        order_task.save()

    def form_valid(self, form):
        form.save()
        obj_order_task = self.order_task_form(self.request.POST, user=self.request.user)
        if obj_order_task.is_valid():
            order_task = obj_order_task.save(commit=False)
            order_task.order_id = self.kwargs['pk']
            order_task.created_by = self.request.user
            order_task.process = OrderTask.OPEN
            order_task.save()
            self.process()
        return super(EvaluationView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EvaluationView, self).get_context_data()
        context['order_task'] = self.order_task_form(user=self.request.user)
        return context

    def get_form_kwargs(self):
        kwargs = super(EvaluationView, self).get_form_kwargs()
        kwargs['pk'] = self.kwargs['pk']
        kwargs['task_id'] = self.kwargs['task_id']
        return kwargs


class STLView(TemplateView):
    template_name = 'owners/stl_view.html'


class TLView(TemplateView):
    template_name = 'owners/tl_view.html'


def logout_user(request):
    logout(request)
    return redirect('/order/home')
