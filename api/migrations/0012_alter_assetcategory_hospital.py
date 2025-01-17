# Generated by Django 5.1.4 on 2025-01-15 12:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_rename_assetcategroy_assetcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetcategory',
            name='hospital',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asset_category', to='api.hospital'),
        ),
    ]