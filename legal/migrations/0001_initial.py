# Generated by Django 4.0.1 on 2022-08-25 07:02

import ckeditor.fields
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LegalDocs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc_name', models.CharField(blank=True, max_length=100)),
                ('doc_text', ckeditor.fields.RichTextField(blank=True)),
                ('doc_id', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Legal Documents',
            },
        ),
        migrations.CreateModel(
            name='RecruitmentLegalDoc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to='Recruitment_docs/')),
                ('doc_type', models.SmallIntegerField(choices=[(1, 'Candidate Consent Form'), (2, 'DriverHealth Terms of Engagement'), (3, 'Other'), (4, 'Service Level Agreement')])),
                ('other_doc', models.CharField(blank=True, max_length=300)),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name_plural': 'Recruitment Documents',
            },
        ),
    ]
