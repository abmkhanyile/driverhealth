# Generated by Django 4.0.1 on 2022-09-30 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training_courses', '0016_alter_trainingdays_training_slot'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainingcourse',
            name='elearning',
            field=models.BooleanField(default=False),
        ),
    ]
