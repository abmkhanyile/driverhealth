# Generated by Django 4.0.5 on 2022-06-25 11:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('countries', '0001_initial'),
        ('user_accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DHClient',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('has_passport', models.BooleanField(default=False)),
                ('passport_num', models.CharField(blank=True, max_length=30)),
                ('location', models.CharField(max_length=150)),
                ('post_code', models.CharField(blank=True, max_length=15)),
                ('rating', models.SmallIntegerField(choices=[(0, '0 Star'), (1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')], default=0, null=True)),
                ('dh_test_comment', models.CharField(blank=True, max_length=1500)),
                ('tested', models.BooleanField(blank=True, default=False)),
                ('in_job_market', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('nationality', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='countries.country')),
            ],
            options={
                'verbose_name_plural': 'DH Clients',
            },
        ),
    ]