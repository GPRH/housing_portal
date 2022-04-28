# Generated by Django 2.2.12 on 2020-07-30 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0051_update_building_indexes'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='geohash',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddIndex(
            model_name='building',
            index=models.Index(fields=['geohash'],
                               name='geodata_bui_geohash_1f6bec_idx'),
        ),
    ]
