# Generated by Django 4.0.5 on 2022-06-24 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training_courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='code14course',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='trainingcourse',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]