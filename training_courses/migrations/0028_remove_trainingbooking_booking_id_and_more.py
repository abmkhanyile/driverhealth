# Generated by Django 4.0.1 on 2022-10-09 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('training_courses', '0027_alter_bookingtransaction_trans_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trainingbooking',
            name='booking_id',
        ),
        migrations.AddField(
            model_name='trainingbooking',
            name='booking_transaction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transaction_bookings', to='training_courses.bookingtransaction'),
        ),
    ]
