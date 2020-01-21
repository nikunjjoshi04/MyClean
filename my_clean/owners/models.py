from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    AGENT = 'agent'
    ADMIN = 'admin'
    EVALUATOR = 'evaluator'
    STL = 'stl'
    TL = 'tl'
    ACCOUNTENT = 'accountent'
    user_choices = [
        (AGENT, 'Agent'),
        (ADMIN, 'Admin'),
        (EVALUATOR, 'Evaluator'),
        (STL, 'STL'),
        (TL, 'TL'),
        (ACCOUNTENT, 'Accountent'),
    ]
    user_type = models.CharField(max_length=20, choices=user_choices)


class TeamMembers(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    Mobile_no = models.CharField(max_length=10)

    def __str__(self):
        return '{} - {}'.format(self.first_name, self.last_name)
