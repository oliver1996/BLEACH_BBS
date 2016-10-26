# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybbs', '0002_auto_20150729_0115'),
    ]

    operations = [
        migrations.AddField(
            model_name='bbs',
            name='cai_id',
            field=models.TextField(default=','),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bbs',
            name='zan_id',
            field=models.TextField(default=','),
            preserve_default=True,
        ),
    ]
