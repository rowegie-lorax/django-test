# Generated by Django 2.0.13 on 2019-05-05 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20190505_2218'),
    ]

    operations = [
        migrations.AddField(
            model_name='shift',
            name='time_in',
            field=models.TimeField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='shift',
            name='time_out',
            field=models.TimeField(blank=True, db_index=True, null=True),
        ),
    ]