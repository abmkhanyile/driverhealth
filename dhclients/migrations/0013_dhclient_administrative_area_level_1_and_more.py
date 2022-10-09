# Generated by Django 4.0.1 on 2022-08-28 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dhclients', '0012_remove_dhclient_location_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='dhclient',
            name='administrative_area_level_1',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='dhclient',
            name='administrative_area_level_2',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='dhclient',
            name='country',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='dhclient',
            name='locality',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='dhclient',
            name='sublocality',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='dhclient',
            name='postal_code',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]