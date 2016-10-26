# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybbs', '0004_auto_20150731_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='bbs_user',
            name='favor',
            field=models.TextField(default='x'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bbs_user',
            name='photo',
            field=models.ImageField(upload_to='head', default='head/photo.jpg'),
            preserve_default=True,
        ),
    ]
