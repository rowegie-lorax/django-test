# Generated by Django 2.0.13 on 2019-04-28 07:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_filedirectory_uploaded_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileViews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_views', models.DecimalField(decimal_places=2, max_digits=10)),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.FileDirectory')),
            ],
        ),
    ]
