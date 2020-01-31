from django.urls import path
from .views import CustomerView


app_name = 'customer'
urlpatterns = [
    path('customer_view/<int:pk>/', CustomerView.as_view(), name='customer_view')
]
