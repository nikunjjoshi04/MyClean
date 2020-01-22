# Generated by Django 3.0.2 on 2020-01-22 08:43

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DustLevelPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dust_level', models.CharField(max_length=50)),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_of_team_members', models.IntegerField()),
                ('expected_time', models.FloatField()),
                ('estimated_price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process', models.CharField(choices=[('in_evaluation', 'In Evaluation Process'), ('in_stl', 'In STL Observation'), ('in_tl', 'In TL Observation'), ('in_payment', 'In Payment Process'), ('order_done', 'Order Done')], max_length=30)),
                ('date', models.DateTimeField(default=datetime.datetime(2020, 1, 22, 8, 43, 12, 854112, tzinfo=utc))),
            ],
        ),
        migrations.CreateModel(
            name='OrderTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process', models.CharField(choices=[('open', 'Open'), ('in_process', 'In Process'), ('finish', 'Finish')], max_length=30)),
                ('date', models.DateTimeField(default=datetime.datetime(2020, 1, 22, 8, 43, 12, 854784, tzinfo=utc))),
            ],
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_type', models.CharField(max_length=50)),
                ('service_price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_id', models.CharField(max_length=50)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Order')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.OrderTask')),
            ],
        ),
    ]
