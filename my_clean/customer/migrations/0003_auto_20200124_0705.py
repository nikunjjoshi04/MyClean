# Generated by Django 3.0.2 on 2020-01-24 07:05

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_auto_20200124_0634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='mobile_no',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=15, region=None),
        ),
    ]
