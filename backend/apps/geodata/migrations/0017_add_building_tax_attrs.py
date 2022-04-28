# Generated by Django 2.1.1 on 2019-10-16 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0016_alter_sv_vintage'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='count',
            field=models.IntegerField(blank=True, help_text='Number of records calculated in\n            average property tax per building', null=True),
        ),
        migrations.AddField(
            model_name='building',
            name='pt_avg',
            field=models.IntegerField(blank=True, help_text='Average property tax per building', null=True),
        ),
        migrations.AddField(
            model_name='building',
            name='pt_avg_owed',
            field=models.IntegerField(blank=True, help_text='Average property tax owed per building', null=True),
        ),
        migrations.AddField(
            model_name='building',
            name='pt_sum',
            field=models.IntegerField(blank=True, help_text='Sum of property tax per building', null=True),
        ),
        migrations.AddField(
            model_name='building',
            name='pt_sum_owed',
            field=models.IntegerField(blank=True, help_text='Sum of property tax owed per building', null=True),
        ),
    ]
