# Generated by Django 4.0.4 on 2022-06-23 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='citas',
            name='asistencia',
            field=models.BooleanField(default=False),
        ),
    ]