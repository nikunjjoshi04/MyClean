# Generated by Django 3.0.2 on 2020-02-03 05:43

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0018_auto_20200131_0902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='evaluation_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 3, 5, 43, 41, 944379, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 3, 5, 43, 41, 942879, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='process',
            field=models.CharField(choices=[('in_evaluation', 'In Evaluation Process'), ('evaluation_done', 'Evaluation Done'), ('in_stl', 'In STL Observation'), ('stl_done', 'STL Process Done'), ('in_cleaning', 'In Cleaning Process'), ('cleaning_done', 'Cleaning Process Done'), ('in_payment', 'In Payment Process'), ('order_done', 'Order Done')], max_length=30),
        ),
        migrations.AlterField(
            model_name='ordertask',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 3, 5, 43, 41, 943665, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='team',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 3, 5, 43, 41, 945027, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='visit',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 3, 5, 43, 41, 946352, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name=datetime.datetime(2020, 2, 3, 5, 43, 41, 946929, tzinfo=utc))),
                ('check_no', models.IntegerField(null=True)),
                ('check_date', models.DateTimeField(null=True)),
                ('bank_name', models.CharField(max_length=150, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Order')),
                ('order_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.OrderTask')),
            ],
        ),
    ]