# Generated by Django 4.0.1 on 2022-10-09 17:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('training_courses', '0025_remove_trainingevent_enrollees'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trans_id', models.CharField(max_length=50)),
                ('trans_tot', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
