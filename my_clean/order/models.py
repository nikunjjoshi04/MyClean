from django.db import models
from django.utils import timezone
from django_fsm import FSMField, transition
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
    IN_CUSTOMER = 'in_customer'
    CUSTOMER_REJECTED = 'customer_rejected'
    CUSTOMER_ACCEPTED = 'customer_accepted'
    IN_TL = 'in_cleaning'
    TL_DONE = 'cleaning_done'
    IN_PAYMENT = 'in_payment'
    ORDER_DONE = 'order_done'
    Process_Flags = [
        (IN_EVALUATION, 'In Evaluation Process'),
        (EVALUATION_DONE, 'Evaluation Done'),
        (IN_STL, 'In STL Observation'),
        (IN_CUSTOMER, 'In Customer Acceptance'),
        (CUSTOMER_REJECTED, 'Customer Rejected'),
        (CUSTOMER_ACCEPTED, 'Customer Accepted'),
        (IN_TL, 'In Cleaning Process'),
        (TL_DONE, 'Cleaning Process Done'),
        (IN_PAYMENT, 'In Payment Process'),
        (ORDER_DONE, 'Order Done'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    process = FSMField(default=IN_EVALUATION, choices=Process_Flags)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='address_pk')
    date = models.DateTimeField(default=timezone.now)
    unique_id = models.CharField(max_length=30)
    description = models.TextField(null=True)

    def __str__(self):
        return '{} - {}'.format(self.unique_id, self.process)

    @transition(field=process, source=IN_CUSTOMER, target=CUSTOMER_REJECTED)
    def customer_rejected(self):
        pass

    @transition(field=process, source=IN_CUSTOMER, target=CUSTOMER_ACCEPTED)
    def customer_accepted(self):
        pass

    @transition(field=process, source=IN_EVALUATION, target=IN_STL)
    def in_stl(self):
        pass

    @transition(field=process, source=[IN_STL, CUSTOMER_REJECTED], target=IN_CUSTOMER)
    def in_customer(self):
        pass

    @transition(field=process, source=CUSTOMER_ACCEPTED, target=IN_TL)
    def in_cleaning(self):
        pass

    @transition(field=process, source=IN_TL, target=TL_DONE)
    def cleaning_done(self):
        pass

    @transition(field=process, source=TL_DONE, target=IN_PAYMENT)
    def in_payment(self):
        pass

    @transition(field=process, source=IN_PAYMENT, target=ORDER_DONE)
    def order_done(self):
        pass


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
    date = models.DateTimeField(default=timezone.now)
    schedule_on = models.DateTimeField(null=True)
    schedule_end = models.DateTimeField(null=True)
    message = models.CharField(max_length=200, null=True)

    def __str__(self):
        return "{} - {} - {}".format(self.order.unique_id, self.process, self.id)


class Evaluation(models.Model):
    CREATED = 'created'
    STL_ACCEPT = 'stl_accept'
    CLIENT_ACCEPT = 'client_accept'
    ACCEPT_FLAGS = [
        (CREATED, 'created'),
        (STL_ACCEPT, 'stl_accept'),
        (CLIENT_ACCEPT, 'client_accept'),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_pk')
    evaluator_order_task = models.ForeignKey(OrderTask, on_delete=models.CASCADE, related_name="evaluator_order_task")
    stl_order_task = models.ForeignKey(OrderTask, on_delete=models.CASCADE, related_name='stl_order_task')
    dust_level = models.ForeignKey(DustLevelPrice, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    team_members = models.IntegerField()
    expected_time = models.DateTimeField()
    estimated_price = models.FloatField()
    evaluation_date = models.DateTimeField(default=timezone.now)
    description = models.TextField(null=True)
    discount = models.IntegerField(null=True)
    accepted = models.CharField(max_length=30, choices=ACCEPT_FLAGS)

    def __str__(self):
        return '{} - {}'.format(self.expected_time, self.estimated_price)


class EvaluationMedia(models.Model):
    image = models.ImageField(upload_to='evaluation/', null=True)
    is_evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, null=True)


class Team(models.Model):
    date = models.DateTimeField(default=timezone.now)
    team_id = models.CharField(max_length=50)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    task = models.ForeignKey(OrderTask, on_delete=models.CASCADE)
    team_leader = models.ForeignKey(User, on_delete=models.CASCADE)
    team_member = models.ManyToManyField(TeamMembers)

    def __str__(self):
        return self.team_id


class Visit(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    order_task = models.ForeignKey(OrderTask, on_delete=models.CASCADE)
    visitor = models.ForeignKey(User, on_delete=models.CASCADE)
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(null=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return '{} - {}'.format(self.order, self.visitor)


class Accounts(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    order_task = models.ForeignKey(OrderTask, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    amount = models.FloatField(null=True)
    check_no = models.IntegerField(null=True)
    check_date = models.DateTimeField(null=True)
    bank_name = models.CharField(max_length=150, null=True)
