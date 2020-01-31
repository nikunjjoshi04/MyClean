from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from order.models import Order, \
    OrderTask


# Create your views here.


class CustomerView(DetailView):
    template_name = 'customer/customer_view.html'
    model = OrderTask
    context_object_name = 'order'
