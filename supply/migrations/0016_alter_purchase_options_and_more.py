# Generated by Django 4.0.3 on 2022-07-25 18:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('supply', '0015_alter_purchase_product_alter_purchase_token'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='purchase',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='purchase',
            unique_together={('token', 'product')},
        ),
    ]
