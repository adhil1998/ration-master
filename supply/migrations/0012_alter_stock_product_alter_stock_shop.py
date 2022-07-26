# Generated by Django 4.0.3 on 2022-07-24 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_alter_member_card'),
        ('supply', '0011_alter_monthlyquota_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock', to='supply.product'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock', to='accounts.rationshop'),
        ),
    ]
