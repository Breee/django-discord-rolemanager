# Generated by Django 2.2.4 on 2019-08-28 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0003_auto_20190828_1320'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllowedDiscordServer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server_id', models.CharField(db_index=True, max_length=128)),
                ('name', models.CharField(blank=True, default=None, max_length=128, null=True)),
            ],
        ),
    ]
