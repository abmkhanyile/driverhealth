# Generated by Django 4.0.1 on 2022-08-22 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training_courses', '0012_trainingevent_hourly_training'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainingcourse',
            name='hourly_training',
            field=models.BooleanField(default=False),
        ),
    ]
