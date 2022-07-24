# Generated by Django 4.0.3 on 2022-07-24 15:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_alter_card_card_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='card',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='accounts.card'),
        ),
    ]
