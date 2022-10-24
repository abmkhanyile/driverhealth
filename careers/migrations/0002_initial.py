# Generated by Django 4.0.5 on 2022-06-25 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dhclients', '0001_initial'),
        ('careers', '0001_initial'),
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='applicants',
            field=models.ManyToManyField(blank=True, related_name='applicants', to='dhclients.dhclient'),
        ),
        migrations.AddField(
            model_name='job',
            name='hired_candidate',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='candidate_job_successes', to='dhclients.dhclient'),
        ),
        migrations.AddField(
            model_name='job',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_jobs', to='companies.company'),
        ),
    ]
