# Generated by Django 4.0.3 on 2022-07-24 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('supply', '0009_alter_holidays_holidays_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='monthlyquota',
            unique_together={('product', 'card_type', 'age_group', 'current_year', 'current_month')},
        ),
    ]