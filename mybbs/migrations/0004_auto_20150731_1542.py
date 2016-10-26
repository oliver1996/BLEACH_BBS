# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybbs', '0003_auto_20150731_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bbs',
            name='cai_id',
            field=models.TextField(default='x'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bbs',
            name='zan_id',
            field=models.TextField(default='x'),
            preserve_default=True,
        ),
    ]
