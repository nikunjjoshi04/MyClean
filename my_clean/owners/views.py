from builtins import super
from django.utils import timezone
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, JsonResponse

from django.forms import modelformset_factory, formset_factory
from django.contrib import messages


from django.shortcuts import redirect, render
from django.views.generic.edit import FormView, UpdateView
from django.views.generic import TemplateView, DetailView, ListView, CreateView
from datetime import datetime
from django.contrib.auth import logout, login, authenticate
from .forms import LoginForm, OrderForm, \
    OrderTaskForm, CustomerForm, AddressForm, EvaluationForm, \
    STLReviewForm, PaymentForm, PostForm, ImageForm, TeamForm
from .models import User, Post, Images
from my_clean.settings import EMAIL_HOST_USER
from owners.util import URL
from order.models import Order, \
    OrderTask, Evaluation, \
    Team, Services, \
    DustLevelPrice, Visit, EvaluationMedia


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
                self.success_url = '/owners/stl_task_view'
            elif user.user_type == "tl":
                self.success_url = '/owners/tl_task_view'
            elif user.user_type == "accountent":
                self.success_url = '/owners/account_task_view'
        return super(LoginView, self).form_valid(form)

    def form_invalid(self, form):
        return super(LoginView, self).form_invalid(form)


class AgentView(FormView):
    form_class = CustomerForm
    template_name = 'owners/agent_view.html'
    success_url = '/owners/agent_task_view'
    address_form = AddressForm
    order_form = OrderForm
    order_task_form = OrderTaskForm

    def form_valid(self, form):
        o_id = 'MCL'
        o = Order.objects.latest('date')
        o_id = o_id + str(datetime.now().year) + '0' + str(o.id + 1)
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
                order.unique_id = o_id
                order.save()
                if obj_oder_task_form.is_valid():
                    order_task = obj_oder_task_form.save(commit=False)
                    order_task.order = order
                    order_task.created_by = self.request.user
                    order_task.process = OrderTask.IN_PROCESS
                    order_task.save()
                return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        # print(form.errors, "<<<<<<<<<<"*8)
        return super(AgentView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(AgentView, self).get_context_data()
        context['order'] = self.order_form
        context['order_task'] = self.order_task_form(user=self.request.user)
        context['address'] = self.address_form
        return context


class AgentTaskView(ListView):
    template_name = 'owners/agent_task_view.html'
    model = OrderTask

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AgentTaskView, self).get_context_data()
        context['tasks'] = self.model.objects.filter(created_by=self.request.user).order_by('-date')
        return context


class AgentDetailView(DetailView):
    template_name = 'owners/agent_detail_view.html'
    model = OrderTask
    context_object_name = 'order_task'


class EvaluatorView(ListView):
    template_name = 'owners/evaluator_view.html'
    model = OrderTask
    context_object_name = 'tasks'

    def get_queryset(self):
        return self.model.objects.filter(assigned_to=self.request.user).order_by('-date')


class EvaluationView(FormView):
    form_class = EvaluationForm
    template_name = 'owners/evaluation_view.html'
    success_url = '/owners/evaluator_view'

    def form_valid(self, form):
        eval_form = form.save(commit=False)
        eval_form.save()
        images = list(self.request.FILES.pop("images", None))
        for image in images:
            evaluation_media = EvaluationMedia(image=image, is_evaluation=eval_form)
            evaluation_media.save()
        order = Order.objects.get(id=self.kwargs['pk'])
        order.in_stl()
        order.save()
        order_task = OrderTask.objects.get(id=self.kwargs['task_id'])
        order_task.schedule_end = timezone.now()
        order_task.process = OrderTask.FINISH
        order_task.save()
        return super(EvaluationView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(EvaluationView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['pk'] = self.kwargs['pk']
        kwargs['task_id'] = self.kwargs['task_id']
        return kwargs

    def form_invalid(self, form):
        # print(form.errors)
        return super(EvaluationView, self).form_invalid(form)


class EvaluatorDetailView(TemplateView):
    template_name = 'owners/evaluator_detail_view.html'

    def get_context_data(self, **kwargs):
        context = super(EvaluatorDetailView, self).get_context_data()
        context['evaluation'] = Evaluation.objects.get(evaluator_order_task=kwargs['id'])
        return context


class STLTaskView(TemplateView):
    template_name = 'owners/stl_task_view.html'
    model = Evaluation

    def get_context_data(self, **kwargs):
        context = super(STLTaskView, self).get_context_data()
        context['tasks'] = self.model.objects.filter(assigned_to=self.request.user).order_by('-id')
        return context


class STLReview(UpdateView):
    template_name = 'owners/stl_review.html'
    form_class = STLReviewForm
    model = Evaluation
    success_url = '/owners/stl_task_view'

    def form_valid(self, form):
        schedule_on = form.cleaned_data['expected_time']
        instance = form.save(commit=False)
        instance.accepted = Evaluation.STL_ACCEPT
        instance.order.in_customer()
        instance.order.save()
        data = URL.encryption(self, pk=instance.order.id)
        print("B_SEND :-  ", data)
        msg = 'http://127.0.0.1:8000/customer/customer_view/' + str(data)
        email = 'nikunj.joshi@trootech.com'
        email1 = instance.order.customer.email
        send_mail("Customer Test", msg, EMAIL_HOST_USER, [email, email1], fail_silently=False)
        instance.save()
        return super(STLReview, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(STLReview, self).get_context_data()
        context['evaluation'] = self.model.objects.get(stl_order_task=self.kwargs['task_id'])
        return context


class STLDetailView(FormView):
    template_name = 'owners/stl_detail_view.html'
    model = OrderTask
    form_class = TeamForm
    success_url = '/owners/stl_task_view'

    def form_valid(self, form):
        team_leader = form.cleaned_data['team_leader']
        team = form.save(commit=False)
        o = Team.objects.latest('date')
        o_id = 'TEAM' + str(datetime.now().year) + '0' + str(o.id + 1)
        task = OrderTask.objects.get(id=self.request.session['team'])
        print('team_id', o.id)
        print(task.order, o_id)
        team.team_id = o_id
        team.order = task.order
        task.process = OrderTask.FINISH
        task.order.in_cleaning()
        task.order.save()
        task.save()
        tl_task = OrderTask.objects.create(
            order=task.order,
            created_by=self.request.user,
            assigned_to=team_leader,
            process=OrderTask.IN_PROCESS,
        )
        team.task = tl_task
        team.save()
        return super(STLDetailView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(STLDetailView, self).get_context_data()
        self.request.session['team'] = self.kwargs['pk']
        context['order_task'] = self.model.objects.get(id=self.request.session['team'])
        print(self.kwargs['pk'])
        return context


def stl_calc(request):
    members = request.GET['members']
    dust_level = request.GET['dust_level']
    discount = request.GET['discount']
    dust_price = DustLevelPrice.objects.get(dust_level=dust_level)
    if discount is "" or int(discount) < 0:
        discount = 0
    price = (dust_price.price * int(members)) - int(discount)
    return JsonResponse({'price': str(price)})


class TLTaskView(ListView):
    template_name = 'owners/tl_task_view.html'
    model = OrderTask

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TLTaskView, self).get_context_data()
        context['tasks'] = self.model.objects.filter(assigned_to=self.request.user).order_by('-date')
        return context


class TLDetailView(DetailView):
    template_name = 'owners/tl_detail_view.html'
    model = OrderTask
    context_object_name = 'order_task'


def tl_start(request):
    task_id = request.GET['task_id']
    task = OrderTask.objects.get(id=task_id)
    order = Order.objects.get(id=task.order.id)
    order.process = Order.IN_TL
    order.save()
    visit = Visit.objects.create(
        order=task.order,
        order_task=task,
        visitor=request.user,
        start=timezone.now(),
        team=task.order.team_set.first()
    )
    return JsonResponse({'visit_id': visit.id})


def tl_end(request):
    visit_id = request.GET['visit_id']
    visit = Visit.objects.get(id=visit_id)
    visit.end = timezone.now()
    order = Order.objects.get(id=visit.order.id)
    order.process = Order.TL_DONE
    order.save()
    task = OrderTask.objects.get(id=visit.order_task.id)
    task.process = OrderTask.FINISH
    task.save()
    visit.save()
    user = User.objects.get(user_type='accountent')
    order_task = OrderTask.objects.create(
        order=order,
        created_by=request.user,
        assigned_to=user,
        process=OrderTask.IN_PROCESS
    )
    return JsonResponse({'visit_id': visit.id})


class AccountTaskView(ListView):
    template_name = 'owners/account_task_view.html'
    model = OrderTask

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AccountTaskView, self).get_context_data()
        context['tasks'] = self.model.objects.filter(assigned_to=self.request.user).order_by('-date')
        return context


class AccountDetailView(FormView):
    template_name = 'owners/account_detail_view.html'
    form_class = PaymentForm
    success_url = '/owners/account_task_view'

    def get_context_data(self, **kwargs):
        context = super(AccountDetailView, self).get_context_data()
        context['order_task'] = OrderTask.objects.get(id=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.save()
        return super(AccountDetailView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(AccountDetailView, self).get_form_kwargs()
        kwargs['task_id'] = self.kwargs['pk']
        return kwargs

    def form_invalid(self, form):
        print(form.errors)
        return super(AccountDetailView, self).form_invalid(form)


def logout_user(request):
    logout(request)
    return redirect('/order/home')


def post(request):

    ImageFormSet = modelformset_factory(Images,form=ImageForm, extra=3)

    #'extra' means the number of photos that you can upload   ^

    if request.method == 'POST':

        postForm = PostForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=Images.objects.none())


        if postForm.is_valid() and formset.is_valid():
            post_form = postForm.save(commit=False)
            post_form.user = request.user
            post_form.save()

            for form in formset.cleaned_data:
                #this helps to not crash if the user
                #do not upload all the photos
                if form:
                    image = form['image']
                    photo = Images(post=post_form, image=image)
                    photo.save()
            messages.success(request,
                             "Yeeew, check it out on the home page!")
            return HttpResponseRedirect("/")
        else:
            print(postForm.errors, formset.errors)
    else:
        postForm = PostForm()
        formset = ImageFormSet(queryset=Images.objects.none())
    return render(request, 'owners/blog.html',
                  {'postForm': postForm, 'formset': formset})