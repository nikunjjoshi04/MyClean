from django.db import models
from customer.models import Customer
from owners.models import User, TeamMembers


# Create your models here.


class Services(models.Model):
    service_type = models.CharField(max_length=50)
    service_price = models.FloatField()

    def __str__(self):
        return self.service_type


class DustLevelPrice(models.Model):
    dust_level = models.CharField(max_length=50)
    price = models.FloatField()

    def __str__(self):
        return self.dust_level


class Order(models.Model):
    Process_Flags = [
        ('OP', 'On Process'),
        ('EP', 'In Evaluation Process'),
        ('SO', 'In STL Observation'),
        ('TO', 'In TL Observation'),
        ('OC', 'On Cleaning'),
        ('PP', 'In Payment Process'),
        ('OD', 'Order Done'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    process = models.CharField(max_length=2, choices=Process_Flags)

    def __str__(self):
        return self.process


class OrderTask(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    task = models.ForeignKey(User, on_delete=models.CASCADE)
    approve = models.BooleanField(default=False)

    def __str__(self):
        return "{} - {}".format(self.order, self.approve)


class Evaluation(models.Model):
    order_task = models.ForeignKey(OrderTask, on_delete=models.CASCADE)
    dust_level = models.ForeignKey(DustLevelPrice, on_delete=models.CASCADE)
    no_of_team_members = models.IntegerField()
    expected_time = models.FloatField()
    estimated_price = models.FloatField()

    def __str__(self):
        return '{} - {}'.format(self.expected_time, self.estimated_price)


class Team(models.Model):
    team_id = models.CharField(max_length=50)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    task = models.ForeignKey(OrderTask, on_delete=models.CASCADE)
    team_leader = models.ForeignKey(User, on_delete=models.CASCADE)
    team_member = models.ManyToManyField(TeamMembers)

    def __str__(self):
        return self.team_id
