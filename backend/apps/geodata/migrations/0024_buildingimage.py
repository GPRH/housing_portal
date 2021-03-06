# Generated by Django 2.1.11 on 2019-11-11 17:23

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0023_alter_building_id_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuildingImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('detection_id', models.BigIntegerField(blank=True, null=True)),
                ('image_id', models.BigIntegerField(blank=True, null=True)),
                ('angle', models.FloatField(blank=True, null=True)),
                ('subfolder', models.CharField(blank=True, max_length=255, null=True)),
                ('frame', models.CharField(blank=True, max_length=254, null=True)),
                ('cam', models.BigIntegerField(blank=True, null=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiLineStringField(srid=4326)),
                ('aoi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='images', to='geodata.AOI')),
                ('building', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='images', to='geodata.Building')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('vector_tiles', django.db.models.manager.Manager()),
            ],
        ),
    ]
