# Generated by Django 4.0.1 on 2022-10-18 14:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('training_courses', '0028_remove_trainingbooking_booking_id_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='trainingtime',
            options={'ordering': ('-time_slot',)},
        ),
    ]