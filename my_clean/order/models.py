from django.db import models
from django.utils import timezone
from customer.models import Customer, Address
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
    OPEN = 'open'
    IN_EVALUATION = 'in_evaluation'
    EVALUATION_DONE = 'evaluation_done'
    IN_STL = 'in_stl'
    IN_TL = 'in_tl'
    IN_PAYMENT = 'in_payment'
    ORDER_DONE = 'order_done'
    Process_Flags = [
        (OPEN, 'Open Process'),
        (IN_EVALUATION, 'In Evaluation Process'),
        (EVALUATION_DONE, 'Evaluation Done'),
        (IN_STL, 'In STL Observation'),
        (IN_TL, 'In TL Observation'),
        (IN_PAYMENT, 'In Payment Process'),
        (ORDER_DONE, 'Order Done'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    process = models.CharField(max_length=30, choices=Process_Flags)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='address_pk')
    date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.process


class OrderTask(models.Model):
    OPEN = 'open'
    IN_PROCESS = 'in_process'
    FINISH = 'finish'
    Process_Flags = [
        (OPEN, 'Open'),
        (IN_PROCESS, 'In Process'),
        (FINISH, 'Finish'),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned')
    process = models.CharField(max_length=30, choices=Process_Flags)
    date = models.DateTimeField(default=timezone.now())
    evaluation_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return "{} - {}".format(self.date, self.process)


class Evaluation(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_pk')
    order_task = models.ForeignKey(OrderTask, on_delete=models.CASCADE)
    dust_level = models.ForeignKey(DustLevelPrice, on_delete=models.CASCADE)
    team_members = models.IntegerField()
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
