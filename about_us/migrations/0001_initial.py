# Generated by Django 4.0.1 on 2022-06-26 05:56

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='About_Us',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compName', models.CharField(blank=True, max_length=250)),
                ('compRegNum', models.CharField(blank=True, max_length=30)),
                ('VAT_num', models.CharField(default='Not VAT registered.', max_length=25)),
                ('contactNumber', models.CharField(blank=True, max_length=30)),
                ('faxNumber', models.CharField(blank=True, max_length=30)),
                ('emailAddress', models.CharField(blank=True, max_length=150)),
                ('website', models.CharField(blank=True, max_length=150)),
                ('physicalAddress', ckeditor.fields.RichTextField(blank=True)),
                ('postalAddress', ckeditor.fields.RichTextField(blank=True)),
                ('account_holder', models.CharField(blank=True, max_length=100)),
                ('bankName', models.CharField(blank=True, max_length=100)),
                ('bankAccNum', models.CharField(blank=True, max_length=30)),
                ('accType', models.CharField(blank=True, max_length=30)),
                ('branchName', models.CharField(blank=True, max_length=50)),
                ('branchCode', models.CharField(blank=True, max_length=20)),
                ('swiftCode', models.CharField(blank=True, max_length=20)),
                ('about_us_page_txt', ckeditor.fields.RichTextField()),
                ('about_us_id', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'About Us',
            },
        ),
    ]
