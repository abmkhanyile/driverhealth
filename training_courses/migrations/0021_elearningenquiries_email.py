# Generated by Django 4.0.1 on 2022-10-03 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training_courses', '0020_elearningenquiries_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='elearningenquiries',
            name='email',
            field=models.EmailField(blank=True, max_length=200, null=True),
        ),
    ]
