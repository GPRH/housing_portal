# Generated by Django 2.1.11 on 2019-11-08 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0021_add_sv_lat_lng_aoi'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='building',
            name='fid',
        ),
        migrations.RemoveField(
            model_name='plot',
            name='objectid',
        ),
        migrations.AlterField(
            model_name='building',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]