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
    IN_EVALUATION = 'in_evaluation'
    EVALUATION_DONE = 'evaluation_done'
    IN_STL = 'in_stl'
    STL_DONE = 'stl_done'
    IN_TL = 'in_tl'
    TL_DONE = 'tl_done'
    IN_PAYMENT = 'in_payment'
    ORDER_DONE = 'order_done'
    Process_Flags = [
        (IN_EVALUATION, 'In Evaluation Process'),
        (EVALUATION_DONE, 'Evaluation Done'),
        (IN_STL, 'In STL Observation'),
        (STL_DONE, 'STL Process Done'),
        (IN_TL, 'In TL Observation'),
        (TL_DONE, 'TL Process Done'),
        (IN_PAYMENT, 'In Payment Process'),
        (ORDER_DONE, 'Order Done'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    process = models.CharField(max_length=30, choices=Process_Flags)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='address_pk')
    date = models.DateTimeField(default=timezone.now())
    unique_id = models.CharField(max_length=30)
    description = models.TextField(null=True)

    def __str__(self):
        return '{} - {}'.format(self.unique_id, self.process)


class OrderTask(models.Model):
    IN_PROCESS = 'in_process'
    FINISH = 'finish'
    Process_Flags = [
        (IN_PROCESS, 'In Process'),
        (FINISH, 'Finish'),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned')
    process = models.CharField(max_length=30, choices=Process_Flags)
    date = models.DateTimeField(default=timezone.now())
    schedule_on = models.DateTimeField(null=True)
    schedule_end = models.DateTimeField(null=True)
    message = models.CharField(max_length=200, null=True)

    def __str__(self):
        return "{} - {}".format(self.order.unique_id, self.process)


class Evaluation(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_pk')
    evaluator_order_task = models.ForeignKey(OrderTask, on_delete=models.CASCADE, related_name="evaluator_order_task")
    stl_order_task = models.ForeignKey(OrderTask, on_delete=models.CASCADE, related_name='stl_order_task')
    dust_level = models.ForeignKey(DustLevelPrice, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    team_members = models.IntegerField()
    expected_time = models.DateTimeField()
    estimated_price = models.FloatField()
    evaluation_date = models.DateTimeField(default=timezone.now())
    description = models.TextField(null=True)
    discount = models.IntegerField(null=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return '{} - {}'.format(self.expected_time, self.estimated_price)


class Team(models.Model):
    date = models.DateTimeField(default=timezone.now())
    team_id = models.CharField(max_length=50)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    task = models.ForeignKey(OrderTask, on_delete=models.CASCADE)
    team_leader = models.ForeignKey(User, on_delete=models.CASCADE)
    team_member = models.ManyToManyField(TeamMembers)

    def __str__(self):
        return self.team_id
