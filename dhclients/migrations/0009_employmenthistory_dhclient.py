# Generated by Django 4.0.1 on 2022-07-07 05:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dhclients', '0008_employmenthistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='employmenthistory',
            name='dhclient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client_employment_history', to='dhclients.dhclient'),
        ),
    ]
