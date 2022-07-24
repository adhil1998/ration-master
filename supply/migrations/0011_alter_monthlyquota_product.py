# Generated by Django 4.0.3 on 2022-07-24 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('supply', '0010_alter_monthlyquota_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthlyquota',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quota', to='supply.product'),
        ),
    ]