# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_housecode_temperature_opentrv'),
    ]

    operations = [
        migrations.AlterField(
            model_name='housecode',
            name='temperature_opentrv',
            field=models.CharField(default=None, max_length=6, null=True),
        ),
    ]
