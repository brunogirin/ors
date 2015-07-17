# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_housecode'),
    ]

    operations = [
        migrations.AddField(
            model_name='housecode',
            name='temperature_opentrv',
            field=models.CharField(default=None, max_length=6),
        ),
    ]
