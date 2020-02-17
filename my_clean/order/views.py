from django.shortcuts import render
from django.views.generic.base import TemplateView


# Create your views here.


class HomePageView(TemplateView):
    template_name = 'order/index.html'


class AboutPageView(TemplateView):
    template_name = 'order/about.html'


class ContactPageView(TemplateView):
    template_name = 'order/contact.html'


class GalleryPageView(TemplateView):
    template_name = 'order/gallery.html'
