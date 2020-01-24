from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class State(models.Model):
    state_name = models.CharField(max_length=20)

    def __str__(self):
        return self.state_name


class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=30)

    def __str__(self):
        return self.city_name


class Customer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    # mobile_no = models.CharField(max_length=15)
    mobile_no = PhoneNumberField()
    email = models.EmailField()

    def __str__(self):
        return '{} - {}'.format(self.first_name, self.last_name)


class Address(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    street = models.CharField(max_length=200)
    building = models.CharField(max_length=100)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.building