# Generated by Django 4.0.1 on 2022-11-03 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('training_courses', '0038_trainingdays_selcourse'),
    ]

    operations = [
        migrations.AddField(
            model_name='selectedcourse',
            name='trcourse',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='selected_courses', to='training_courses.trainingcourse'),
        ),
    ]
