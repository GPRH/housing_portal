# Generated by Django 2.2.12 on 2020-07-29 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0050_building_image_cam_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='confidencevalue',
            name='bucket',
            field=models.IntegerField(blank=True, help_text='Bucket to which the confidence value is assigned.', null=True),
        ),
    ]
