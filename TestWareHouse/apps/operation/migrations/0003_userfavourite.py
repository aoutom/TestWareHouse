# Generated by Django 2.2 on 2021-07-01 08:53

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('test', '0008_auto_20210626_1712'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('operation', '0002_auto_20210629_1744'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFavourite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('is_active', models.IntegerField(default=1, verbose_name='是否启用')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='test.Test', verbose_name='题目')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '收藏记录',
                'verbose_name_plural': '收藏记录',
                'unique_together': {('user', 'test')},
            },
        ),
    ]
