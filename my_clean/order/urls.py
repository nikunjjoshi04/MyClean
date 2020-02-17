from django.urls import path
from .views import HomePageView, AboutPageView, ContactPageView, GalleryPageView

app_name = 'order'
urlpatterns = [
    path('home/', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('gallery/', GalleryPageView.as_view(), name='gallery'),
]
