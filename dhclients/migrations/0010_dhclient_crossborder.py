# Generated by Django 4.0.1 on 2022-07-08 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dhclients', '0009_employmenthistory_dhclient'),
    ]

    operations = [
        migrations.AddField(
            model_name='dhclient',
            name='crossborder',
            field=models.BooleanField(default=True),
        ),
    ]
