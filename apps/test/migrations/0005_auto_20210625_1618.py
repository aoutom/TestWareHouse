# Generated by Django 2.2 on 2021-06-25 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test', '0004_auto_20210625_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='select_a',
            field=models.CharField(default='', max_length=50, verbose_name='选项a'),
        ),
        migrations.AlterField(
            model_name='test',
            name='select_b',
            field=models.CharField(default='', max_length=50, verbose_name='选项b'),
        ),
        migrations.AlterField(
            model_name='test',
            name='select_c',
            field=models.CharField(default='', max_length=50, verbose_name='选项c'),
        ),
        migrations.AlterField(
            model_name='test',
            name='select_d',
            field=models.CharField(default='', max_length=50, verbose_name='选项d'),
        ),
        migrations.AlterField(
            model_name='test',
            name='select_e',
            field=models.CharField(default='', max_length=50, verbose_name='选项e'),
        ),
        migrations.AlterField(
            model_name='test',
            name='select_f',
            field=models.CharField(default='', max_length=50, verbose_name='选项f'),
        ),
        migrations.AlterField(
            model_name='test',
            name='select_g',
            field=models.CharField(default='', max_length=50, verbose_name='选项g'),
        ),
        migrations.AlterField(
            model_name='test',
            name='select_h',
            field=models.CharField(default='', max_length=50, verbose_name='选项h'),
        ),
    ]
