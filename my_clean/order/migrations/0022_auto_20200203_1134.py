# Generated by Django 3.0.2 on 2020-02-03 11:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0021_auto_20200203_1134'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounts',
            name='amount',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='accounts',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 3, 11, 34, 40, 951532, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='evaluation_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 3, 11, 34, 40, 949029, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 3, 11, 34, 40, 947584, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='ordertask',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 3, 11, 34, 40, 948339, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='team',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 3, 11, 34, 40, 949688, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='visit',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 3, 11, 34, 40, 950973, tzinfo=utc)),
        ),
    ]
