from django.urls import path
from .views import HomePageView

app_name = 'order'
urlpatterns = [
    path('home/', HomePageView.as_view(), name='home')
]
