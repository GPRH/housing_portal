# Generated by Django 2.2.12 on 2020-08-18 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0055_add_json_gin_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='hz_tsunami',
            field=models.IntegerField(blank=True, help_text='Tsunami risk.', null=True),
        ),
    ]
