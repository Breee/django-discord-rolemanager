# Generated by Django 2.2.4 on 2019-08-29 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0004_alloweddiscordserver'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='monthly_paid',
            field=models.BooleanField(default=False),
        ),
    ]
