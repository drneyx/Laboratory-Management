# Generated by Django 3.1.4 on 2021-04-24 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slb1', '0009_reserve_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserve',
            name='collect',
            field=models.BooleanField(default=False),
        ),
    ]
