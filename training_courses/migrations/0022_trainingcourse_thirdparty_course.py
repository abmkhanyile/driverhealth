# Generated by Django 4.0.1 on 2022-10-03 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training_courses', '0021_elearningenquiries_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainingcourse',
            name='thirdparty_course',
            field=models.BooleanField(default=False),
        ),
    ]