# Generated by Django 5.1.4 on 2025-01-14 07:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_hospitalmodel'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HospitalModel',
            new_name='Hospital',
        ),
    ]
