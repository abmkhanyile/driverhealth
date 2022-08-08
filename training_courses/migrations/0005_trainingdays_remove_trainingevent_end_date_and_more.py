# Generated by Django 4.0.1 on 2022-07-28 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training_courses', '0004_course_enrollees_trainingevent_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingDays',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('training_slot', models.DateTimeField()),
            ],
        ),
        migrations.RemoveField(
            model_name='trainingevent',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='trainingevent',
            name='start_date',
        ),
    ]