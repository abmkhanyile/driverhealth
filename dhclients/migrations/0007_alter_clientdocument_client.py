# Generated by Django 4.0.1 on 2022-06-29 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dhclients', '0006_alter_clientdocument_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientdocument',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client_documents', to='dhclients.dhclient'),
        ),
    ]