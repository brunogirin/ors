# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20150723_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='housecode',
            name='temperature_ds18b20',
            field=models.FloatField(default=None, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='housecode',
            name='temperature_opentrv',
            field=models.FloatField(default=None, null=True, blank=True),
        ),
    ]
