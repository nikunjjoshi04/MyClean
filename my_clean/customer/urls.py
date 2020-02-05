from django.urls import path
from .views import CustomerView, customer_accept


app_name = 'customer'
urlpatterns = [
    path('customer_view/<str:id>/', CustomerView.as_view(), name='customer_view'),
    path('customer_accept/<int:evaluator_id>/', customer_accept, name='customer_accept'),
]
