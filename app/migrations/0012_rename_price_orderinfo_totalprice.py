# Generated by Django 3.2 on 2021-04-21 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_orderinfo_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderinfo',
            old_name='price',
            new_name='totalPrice',
        ),
    ]
