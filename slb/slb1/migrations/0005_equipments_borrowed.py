# Generated by Django 3.1.4 on 2021-04-23 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slb1', '0004_auto_20210423_2228'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipments',
            name='borrowed',
            field=models.BooleanField(default=False),
        ),
    ]
