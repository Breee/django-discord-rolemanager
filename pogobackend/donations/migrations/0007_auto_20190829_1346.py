# Generated by Django 2.2.4 on 2019-08-29 13:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0006_auto_20190829_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='last_payment',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
