# Generated by Django 4.0.1 on 2022-08-27 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dhclients', '0011_dhclient_location_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dhclient',
            name='location_id',
        ),
    ]
