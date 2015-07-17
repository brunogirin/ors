# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20150717_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='housecode',
            name='last_updated',
            field=models.DateTimeField(default=None, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='housecode',
            name='last_updated_temperatures',
            field=models.DateTimeField(default=None, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='housecode',
            name='window',
            field=models.CharField(default=b'closed', max_length=6, choices=[(b'open', b'open'), (b'closed', b'closed')]),
        ),
    ]
