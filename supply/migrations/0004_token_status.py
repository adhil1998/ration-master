# Generated by Django 4.0.3 on 2022-07-23 18:58

from django.db import migrations, models
import supply.constants


class Migration(migrations.Migration):

    dependencies = [
        ('supply', '0003_remove_stock_unit_product_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='status',
            field=models.IntegerField(choices=[(100, 'INITIATED'), (200, 'COMPLETED'), (300, 'CANCELED')], default=supply.constants.TokenStatus['INITIATED']),
        ),
    ]
