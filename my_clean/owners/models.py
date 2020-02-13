from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify

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


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    body = models.CharField(max_length=400)


def get_image_filename(instance, filename):
    title = instance.post.title
    slug = slugify(title)
    return "post_images/%s-%s" % (slug, filename)


class Images(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None)
    image = models.ImageField(upload_to=get_image_filename, verbose_name='Image')