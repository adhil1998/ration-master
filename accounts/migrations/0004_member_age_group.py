# Generated by Django 4.0.3 on 2022-07-23 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_otptoken_type_alter_otptoken_otp_member'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='age_group',
            field=models.IntegerField(choices=[(100, 'ADULT'), (200, 'CHILD')], default=None),
        ),
    ]
