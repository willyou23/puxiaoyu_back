# Generated by Django 3.2 on 2021-04-17 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_orderinfo_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderinfo',
            name='removal',
            field=models.BooleanField(default=False),
        ),
    ]
