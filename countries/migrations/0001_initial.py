# Generated by Django 4.0.5 on 2022-06-25 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('long_name', models.CharField(max_length=150)),
                ('short_name', models.CharField(blank=True, max_length=10)),
                ('general_coordinates', models.CharField(blank=True, max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Countries',
            },
        ),
    ]
