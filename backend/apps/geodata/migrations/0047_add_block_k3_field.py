# Generated by Django 2.2.12 on 2020-05-19 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0046_update_aoi_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='block',
            name='k3',
            field=models.FloatField(blank=True, help_text='COVID-19 Vulnerability Index', null=True),
        ),
        migrations.AddIndex(
            model_name='block',
            index=models.Index(fields=['k3'], name='geodata_blo_k3_b08be3_idx'),
        ),
    ]
