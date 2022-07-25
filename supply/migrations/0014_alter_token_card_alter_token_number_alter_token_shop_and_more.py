# Generated by Django 4.0.3 on 2022-07-24 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_alter_member_card'),
        ('supply', '0013_remove_token_rationshop_token_shop_alter_token_card'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='card',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='toke', to='accounts.card'),
        ),
        migrations.AlterField(
            model_name='token',
            name='number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='token',
            name='shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='toke', to='accounts.rationshop'),
        ),
        migrations.AlterField(
            model_name='token',
            name='time',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
