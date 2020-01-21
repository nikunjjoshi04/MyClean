from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic import TemplateView, ListView
from .forms import LoginForm, SearchForm
from django.contrib.auth import logout, login, authenticate
from customer.models import Customer, Address, \
    City, State
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


class AgentView(ListView):
    pass


class EvaluatorView(TemplateView):
    template_name = 'owners/evaluator_view.html'


class STLView(TemplateView):
    template_name = 'owners/stl_view.html'


class TLView(TemplateView):
    template_name = 'owners/tl_view.html'


def logout_user(request):
    logout(request)
    return redirect('/order/home')
