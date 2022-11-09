# Generated by Django 4.0.1 on 2022-11-03 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('training_courses', '0036_delete_course_enrollees'),
    ]

    operations = [
        migrations.AddField(
            model_name='selectedcourse',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_courses', to='training_courses.trainingevent'),
        ),
    ]