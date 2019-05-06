# Generated by Django 2.0.13 on 2019-05-05 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20190505_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shifthandover',
            name='comments',
            field=models.ManyToManyField(to='api.GeneralComment'),
        ),
        migrations.AlterField(
            model_name='shifthandover',
            name='incidents',
            field=models.ManyToManyField(to='api.Incident'),
        ),
        migrations.AlterField(
            model_name='shifthandover',
            name='shift_members',
            field=models.ManyToManyField(related_name='shift_members', to='api.User'),
        ),
    ]