# Generated by Django 2.2 on 2021-06-25 15:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='select_i',
        ),
    ]
