from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    user_choices = [
        ('AG', 'Agent'),
        ('AD', 'Admin'),
        ('EV', 'Evaluator'),
        ('ST', 'STL'),
        ('TL', 'TL'),
        ('AC', 'Accountent'),
    ]
    user_type = models.CharField(max_length=2, choices=user_choices)


class TeamMembers(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    Mobile_no = models.CharField(max_length=10)

    def __str__(self):
        return '{} - {}'.format(self.first_name, self.last_name)
