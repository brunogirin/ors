# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20150814_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='housecode',
            name='last_switch_status',
            field=models.CharField(default=None, max_length=3, null=True, blank=True, choices=[(b'on', b'on'), (b'off', b'off')]),
        ),
    ]
