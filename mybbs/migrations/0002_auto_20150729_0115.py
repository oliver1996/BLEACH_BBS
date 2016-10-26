# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybbs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bbs',
            name='cai_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bbs',
            name='com_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bbs',
            name='zan_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
