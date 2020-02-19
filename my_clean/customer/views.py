from django.shortcuts import render, redirect
from .util import URL
from django.views.generic import TemplateView, DetailView
from order.models import Order, \
    OrderTask, Evaluation


# Create your views here.


class CustomerView(TemplateView):
    template_name = 'customer/customer_view.html'

    def get_context_data(self, **kwargs):
        context = super(CustomerView, self).get_context_data()
        data = kwargs.pop('id', None)
        value = URL.decryption(self, data=data)
        id = value['pk']
        context['order'] = Order.objects.get(id=id)
        return context


def customer_accept(request, evaluator_id):
    instance = Evaluation.objects.get(id=evaluator_id)
    instance.accepted = Evaluation.CLIENT_ACCEPT
    instance.order.customer_accepted()
    instance.order.save()
    instance.save()
    return redirect('/order/home')


def customer_reject(request, evaluator_id):
    instance = Evaluation.objects.get(id=evaluator_id)
    instance.accepted = Evaluation.CLIENT_ACCEPT
    instance.order.customer_rejected()
    instance.stl_order_task.process = OrderTask.FINISH
    instance.stl_order_task.save()
    instance.order.save()
    instance.save()
    return redirect('/order/home')
