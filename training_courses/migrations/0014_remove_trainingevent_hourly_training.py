# Generated by Django 4.0.1 on 2022-08-22 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('training_courses', '0013_trainingcourse_hourly_training'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trainingevent',
            name='hourly_training',
        ),
    ]
