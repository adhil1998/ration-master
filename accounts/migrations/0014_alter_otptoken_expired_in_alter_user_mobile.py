# Generated by Django 4.0.3 on 2022-07-23 13:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_alter_otptoken_expired_in'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='expired_in',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 23, 19, 17, 33, 650365)),
        ),
        migrations.AlterField(
            model_name='user',
            name='mobile',
            field=models.CharField(default='', max_length=15, unique=True),
        ),
    ]
