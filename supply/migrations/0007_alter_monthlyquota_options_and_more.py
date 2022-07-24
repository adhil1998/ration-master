# Generated by Django 4.0.3 on 2022-07-24 07:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('supply', '0006_alter_monthlyquota_month'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='monthlyquota',
            options={},
        ),
        migrations.AddField(
            model_name='monthlyquota',
            name='current_month',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='monthlyquota',
            name='current_year',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='monthlyquota',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='monthlyquota',
            unique_together={('product', 'quantity', 'card_type', 'age_group', 'current_year', 'current_month')},
        ),
        migrations.RemoveField(
            model_name='monthlyquota',
            name='month',
        ),
    ]
