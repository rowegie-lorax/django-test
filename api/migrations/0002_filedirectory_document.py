# Generated by Django 2.0.13 on 2019-04-28 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='filedirectory',
            name='document',
            field=models.FileField(null=True, upload_to='documents/'),
        ),
    ]
