# Generated by Django 4.0.1 on 2022-10-20 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0004_company_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='driver_requests_limit',
            field=models.SmallIntegerField(default=10),
        ),
    ]
