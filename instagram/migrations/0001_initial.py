# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-07 05:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('title', models.CharField(max_length=60, null=True)),
                ('time_created', models.DateTimeField(auto_now=True)),
                ('likes', models.IntegerField(default=0, null=True)),
                ('caption', models.CharField(default='', max_length=140)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='yg', to=settings.AUTH_USER_MODEL)),
                ('user_profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.Profile')),
            ],
        ),
    ]
