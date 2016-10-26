# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BBS',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=64)),
                ('summary', models.CharField(max_length=256, blank=True, null=True)),
                ('content', models.TextField()),
                ('view_count', models.IntegerField()),
                ('ranking', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BBS_user',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('signature', models.CharField(max_length=128, default='This guy is too lazy to leave anything here.')),
                ('photo', models.ImageField(upload_to='image/', default='image/photo.jpg')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=32, unique=True)),
                ('administrator', models.ForeignKey(to='mybbs.BBS_user')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='bbs',
            name='author',
            field=models.ForeignKey(to='mybbs.BBS_user'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bbs',
            name='category',
            field=models.ForeignKey(to='mybbs.Category'),
            preserve_default=True,
        ),
    ]
