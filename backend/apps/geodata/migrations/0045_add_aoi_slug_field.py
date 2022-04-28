# Generated by Django 2.1.11 on 2020-04-27 12:18

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0044_revert_decimal_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='aoi',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from=['name']),
        ),
        migrations.AddIndex(
            model_name='aoi',
            index=models.Index(fields=['slug'], name='geodata_aoi_slug_182f57_idx'),
        ),
    ]
