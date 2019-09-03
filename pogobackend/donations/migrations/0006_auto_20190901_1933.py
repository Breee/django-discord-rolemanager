# Generated by Django 2.2.4 on 2019-09-01 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0005_donation_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donator',
            name='balance',
        ),
        migrations.AlterField(
            model_name='donator',
            name='fee',
            field=models.FloatField(default=2.0),
        ),
    ]