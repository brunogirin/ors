# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20150720_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='housecode',
            name='switch',
            field=models.CharField(default=None, max_length=3, null=True, blank=True, choices=[(b'on', b'on'), (b'off', b'off')]),
        ),
        migrations.AlterField(
            model_name='housecode',
            name='synchronising',
            field=models.CharField(default=None, max_length=3, null=True, blank=True, choices=[(b'on', b'on'), (b'off', b'off')]),
        ),
    ]
