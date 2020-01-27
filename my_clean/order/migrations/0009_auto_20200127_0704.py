# Generated by Django 3.0.2 on 2020-01-27 07:04

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0008_auto_20200127_0538'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluation',
            name='assigned_to',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='evaluation_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 27, 7, 4, 23, 146312, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 27, 7, 4, 23, 144888, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='ordertask',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 27, 7, 4, 23, 145631, tzinfo=utc)),
        ),
    ]