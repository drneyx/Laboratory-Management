# Generated by Django 3.1.4 on 2021-04-24 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slb1', '0008_remove_reserve_date_returned'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserve',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
