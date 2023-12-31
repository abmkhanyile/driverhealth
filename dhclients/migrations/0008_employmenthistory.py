# Generated by Django 4.0.1 on 2022-07-07 04:48

import ckeditor.fields
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dhclients', '0007_alter_clientdocument_client'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmploymentHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=150)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('role', models.CharField(max_length=100)),
                ('duties', ckeditor.fields.RichTextField()),
                ('contact_person', models.CharField(max_length=50)),
                ('contact_num', models.CharField(max_length=50)),
                ('contact_permission', models.BooleanField()),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
